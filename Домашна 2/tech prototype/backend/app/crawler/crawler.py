
from bs4 import BeautifulSoup
from datetime import timedelta, date
from app.crawler.helpers import (transform_commas_and_dots,split_date_range,
                     transform_commas_and_append_00, eu_format_to_isoformat, isoformat_to_eu_format, us_format_to_eu_format,eu_format_to_datetime, datetime_to_eu_format, us_to_datetime, us_to_iso_format)
from app.crawler.config import DATA_CSV, BASE_URL, HEADERS

# Helper function for missing data fetch in Filter 3
async def fetch_company_data(session, company_name, start_date):
    end_date = (date.today())
    is_first_time = False
    data_to_append = []

    if(start_date == None):
        start_date = end_date - timedelta(days=365 * 10)
        is_first_time = True
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
                    if is_first_time == False:
                        dates = [eu_format_to_isoformat(row["date"]) for row in data]
                        max_date = max(dates)

                        if max_date > latest_date:
                            latest_date = max_date
                        elif max_date == latest_date:
                            break

                    data_to_append.extend(data)

                    # print(f"Fetched data for {company_name} from {us_format_to_eu_format(from_date)} to {us_format_to_eu_format(to_date)}. Skipped rows with missing data.")
            else:
                print(f"Failed to fetch data for {company_name} from {from_date} to {to_date}.")
    #if data_to_append:
        #append_data_to_db(data_to_append)

    return company_name, isoformat_to_eu_format(end_date.isoformat()), data_to_append


# Helper function
def scrape_data(page_content, company_name):
    soup = BeautifulSoup(page_content, 'html.parser')
    rows = soup.select('tbody > tr')

    data = [
        {
            "company": company_name,
            "date": us_format_to_eu_format(cells[0].text),
            "closing_price": transform_commas_and_dots(cells[1].text),
            "max_price": transform_commas_and_dots(cells[2].text),
            "min_price": transform_commas_and_dots(cells[3].text),
            "avg_price": transform_commas_and_dots(cells[4].text),
            "percentage_change": cells[5].text.replace(".", ","),
            "volume": cells[6].text,
            "total_turnover": transform_commas_and_append_00(cells[8].text)
        }
        for row in rows
        if (cells := row.find_all('td')) # and cells[8].text != '0'
    ]

    return data