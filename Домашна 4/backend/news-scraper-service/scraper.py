from datetime import timedelta, date
from config import BASE_URL
from helpers import extract_news_links, fetch_content, detect_garbled_text

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


