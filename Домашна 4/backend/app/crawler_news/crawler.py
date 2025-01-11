from bs4 import BeautifulSoup
from datetime import timedelta, date, datetime
from io import BytesIO
import fitz
import re
from googletrans import Translator
from crawler_news.config import BASE_URL, HEADERS, CONTENT_URL, ATTACHMENT_URL
from docx import Document

# Helper function for missing data fetch in Filter 3
async def fetch_company_news_data(session, company_name, start_date):
    data_to_append = []

    if (start_date == None):
        end_date = (date.today())
        start_date = (end_date - timedelta(days=365 * 10)).isoformat()
    else:
        start_date = str(start_date)

    latest_date = start_date

    news_date_link = []
    CUSTOM_URL = BASE_URL + f"{company_name}"
    async with session.get(CUSTOM_URL) as response:
        if response.status == 200:
            page_content = await response.text()
            news_date_link = extract_news_links(page_content)
        else:
            print(f"News Crawler - Filter 3: Failed to fetch data. Status code: {response.status}")
            return company_name, None, None

    if not news_date_link:
        return company_name, None, None

    max_date_dict = max(news_date_link, key=lambda x: x['Date'])
    max_date = max_date_dict['Date']

    # print(f"max_date: {max_date}, latest_date: {latest_date}")
    # print(f"Type of max_date: {type(max_date)}, Type of latest_date: {type(latest_date)}")

    if max_date == latest_date:
        return company_name, latest_date, None
    elif max_date > latest_date:

        filtered_list = [entry for entry in news_date_link if entry['Date'] > latest_date]
        latest_date = max_date

        for entry in filtered_list:
            URL = entry['ContentURL']
            async with session.get(URL) as response:
                response_json = await response.json()
                text = await fetch_content(session, response_json)
                if text == "" or text is None or detect_garbled_text(text):
                    continue
                new_data = {
                    "company": company_name,
                    "date": entry['Date'],
                    "content": text,
                    "sentiment": ""
                }
                data_to_append.append(new_data)

    return company_name, latest_date, data_to_append

def convert_to_iso(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    return date_obj.strftime('%Y-%m-%d')

def extract_news_links(page_content):
    list = []
    soup = BeautifulSoup(page_content, 'html.parser')
    news_links = soup.select('#seiNetIssuerLatestNews .container-seinet a')
    for row in news_links:
        news_id = row["href"].split("/")[-1]
        date = str(row.select_one('h4').text.split()[0])

        news_dict = {
            "Date": convert_to_iso(date),
            "ContentURL": CONTENT_URL + f"/{news_id}"
        }
        list.append(news_dict)

    return list

def format_html_text(html_content):
    if not html_content:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace("\xa0", " ")
    return text

def format_PDF_text(text):
    if not text:
        return None
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("\n", " ").strip()
    return text


def extract_text_from_pdf(byte_code):
    if not byte_code:
        return None

    try:
        file = fitz.open(stream=byte_code)
        text = ""
        for page_num in range(min(2, file.page_count)):
            page = file.load_page(page_num)
            text += page.get_text("text")
        return text
    except Exception as e:
        return None


def extract_text_from_docx(byte_code):
    if not byte_code:
        return None

    try:
        doc = Document(byte_code)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return None

async def fetch_attachment(session, attachment_id, file_type):
    CUSTOM_URL = ATTACHMENT_URL + f"/{attachment_id}"
    async with session.get(CUSTOM_URL) as response:
        if response.status == 200:
            bytes_content = await response.read()
            bytes_data = BytesIO(bytes_content)
            if file_type == "pdf":
                text = format_PDF_text(extract_text_from_pdf(bytes_data))
            elif file_type == "docx":
                text = format_PDF_text(extract_text_from_docx(bytes_data))
            return text
    return None

def extract_first_link_from_href(text):
    if not text:
        return None
    soup = BeautifulSoup(text, 'lxml')

    link = soup.find('a', href=lambda href: href and href.strip().startswith(
        ('https://seinet.com.mk/document/', 'https://www.seinet.com.mk/document/')))

    return link['href'] if link else None

async def fetch_content(session, response_json, is_redirect=False):
    content = response_json.get("data", {}).get("attachments", None)
    if content:
        attachment_id = content[0].get("attachmentId", None)
        attachment_type = content[0].get("attachmentType", {}).get("mimeType", "")
        if attachment_id is not None:
            if attachment_type == "application/pdf":
                return await fetch_attachment(session, attachment_id, "pdf")
            elif attachment_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return await fetch_attachment(session, attachment_id, "docx")
            else:
                return None

    text = response_json.get("data", {}).get("content", None)

    if text is None:
        return None

    # Check if redirection is needed
    url_check = extract_first_link_from_href(text)
    if url_check:
        news_id = url_check.split("/")[-1]
        url = CONTENT_URL + f"/{news_id}"
        async with session.get(url) as response:
            if response.status == 200:
                response_json_redirect = await response.json()
                content_mk = await fetch_content(session, response_json_redirect)
                #return content_mk
                if content_mk:
                    return translate_mk_to_en(translator, content_mk)
                else:
                    return None

    if text:
        return format_html_text(text)
    else:
        return None

translator = Translator()

def translate_mk_to_en(translator, text):
    if text is not None:
        if isinstance(text, str) and text.strip():
            if "..." in text:
                return None

            normalized_text = normalize_cyrillic(text)
            try:
                max_length = 5000
                if len(normalized_text) > max_length:
                    parts = [normalized_text[i:i + max_length] for i in range(0, len(normalized_text), max_length)]
                    translated_parts = [translator.translate(part, src='mk', dest='en').text for part in parts]
                    return ' '.join(translated_parts)

                detected_lang = translator.detect(normalized_text).lang
                if detected_lang == 'mk':
                    return translator.translate(normalized_text, src='mk', dest='en').text
                return normalized_text
            except Exception as e:
                return normalized_text
    else:
        return None

def normalize_cyrillic(text):
    replacements = {
        '~': 'ч', '{': 'ш', '}': 'ж', '`': 'ѓ', ']': 'љ', '[': 'њ', '|': 'и',
        '@': 'џ', '^': 'ќ',
        'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е', 'Z': 'З',
        'I': 'И', 'J': 'Ј', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О',
        'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'F': 'Ф', 'H': 'Х',
        'C': 'Ц', 'Y': 'Ч', 'X': 'Џ', 'Q': 'Ш',
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'z': 'з',
        'i': 'и', 'j': 'ј', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
        'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х',
        'c': 'ц', 'y': 'ч', 'x': 'џ', 'q': 'ш'
    }
    for latin_char, cyrillic_char in replacements.items():
        text = text.replace(latin_char, cyrillic_char)
    return text

def detect_garbled_text(text):
    mixed_words = re.findall(r'\b[A-Za-z]+\d+[A-Za-z]*\b', text)
    return len(mixed_words) > 10