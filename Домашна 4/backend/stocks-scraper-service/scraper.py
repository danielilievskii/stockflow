
from bs4 import BeautifulSoup
from datetime import timedelta, date
from helpers import (convert_en_to_mk_number_format, split_date_range,
                     standardize_mk_number_format, eu_format_to_iso_format, iso_format_to_eu_format, us_format_to_eu_format, eu_format_to_datetime, datetime_to_eu_format, us_format_to_datetime, us_format_to_iso_format)
from config import BASE_URL, HEADERS

# Helper function for missing data fetch in Filter 3
async def fetch_company_data(session, company_name, start_date):
    end_date = (date.today())
    data_to_append = []

    if(start_date == None):
        start_date = end_date - timedelta(days=365 * 10)
    else:
        start_date = eu_format_to_datetime(start_date)

    latest_date = start_date.isoformat()
    date_ranges = split_date_range(start_date, end_date)

    for from_date, to_date in date_ranges:
        converted_from_date = from_date.replace("/", "%2F")
        converted_to_date = to_date.replace("/", "%2F")
        payload = f"FromDate={converted_from_date}&ToDate={converted_to_date}&Code={company_name}"
        async with session.get(BASE_URL, headers=HEADERS, data=payload) as response:
            if response.status == 200:
                page_content = await response.text()
                data = scrape_data(page_content, company_name)

                if data:
                    data_to_append.extend(data)
                    # print(f"Fetched data for {company_name} from {us_format_to_eu_format(from_date)} to {us_format_to_eu_format(to_date)}. Skipped rows with missing data.")
            else:
                print(f"Failed to fetch data for {company_name} from {from_date} to {to_date}.")

    dates = [eu_format_to_iso_format(row["date"]) for row in data_to_append]
    if dates:
        max_date = max(dates)
        latest_date = (date.fromisoformat(max_date) + timedelta(days=1)).isoformat()
    else: latest_date = start_date.isoformat()

    return company_name, iso_format_to_eu_format(latest_date), data_to_append


# Helper function
def scrape_data(page_content, company_name):
    soup = BeautifulSoup(page_content, 'html.parser')
    rows = soup.select('tbody > tr')

    data = [
        {
            "company": company_name,
            "date": us_format_to_eu_format(cells[0].text),
            "closing_price": convert_en_to_mk_number_format(cells[1].text),
            "max_price": convert_en_to_mk_number_format(cells[2].text),
            "min_price": convert_en_to_mk_number_format(cells[3].text),
            "avg_price": convert_en_to_mk_number_format(cells[4].text),
            "percentage_change": cells[5].text,
            "volume": cells[6].text,
            "total_turnover": standardize_mk_number_format(cells[8].text)
        }
        for row in rows
        if (cells := row.find_all('td'))
    ]

    return data