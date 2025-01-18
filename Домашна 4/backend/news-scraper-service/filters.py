import aiohttp
import asyncio
import multiprocessing
from multiprocessing import Pool, Manager
from bs4 import BeautifulSoup
from datetime import datetime
from scraper import fetch_company_news_data
from config import BASE_URL, COMPANIES_URL, HEADERS
from data_utils import save_latest_dates_to_db, load_latest_dates_from_db, append_data_to_db


# Filter 1: Fetch valid companies
async def filter_1_fetch_companies():
    async with aiohttp.ClientSession() as session:
        async with session.get(COMPANIES_URL, headers=HEADERS) as response:
            page_content = await response.text()
            soup = BeautifulSoup(page_content, 'html.parser')
            companies = [option.text for option in soup.select("select#Code option")
                         if not any(char.isdigit() for char in option.text)]

    print("News Crawler - Filter 1: Fetched companies.")
    return companies


# Filter 2: Initialize latest dates
async def filter_2_initialize_dates(companies):
    company_latest_dates = load_latest_dates_from_db()
    if not company_latest_dates:
        print("News Crawler - Filter 2: No latest dates found in DB. Initializing with None.")
        company_latest_dates = {company: None for company in companies}
    else:
        print("News Crawler - Filter 2: Loaded latest dates from DB.")
    return company_latest_dates


# Filter 3 - Fetch missing data in parallel
def filter_3_fetch_missing_data(company_latest_dates):
    num_cores = multiprocessing.cpu_count()
    chunk_size = max(1, len(company_latest_dates) // num_cores)
    company_chunks = [{k: company_latest_dates[k] for k in list(company_latest_dates)[i:i + chunk_size]}
                      for i in range(0, len(company_latest_dates), chunk_size)]

    with Manager() as manager:
        new_dates = manager.dict()

        with Pool(num_cores) as pool:
            results = pool.map(fetch_data_for_chunk, [(chunk, new_dates) for chunk in company_chunks])

        all_latest_dates = {}
        all_data_to_append = []

        for chunk_new_dates, chunk_data in results:
            all_latest_dates.update(chunk_new_dates)
            all_data_to_append.extend(chunk_data)

        append_data_to_db(all_data_to_append)
        save_latest_dates_to_db(all_latest_dates)

    print("News Crawler - Filter 3: Completed fetching and updating news data.")

def fetch_data_for_chunk(args):
    chunk, _ = args
    async def process_chunk():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_company_news_data(session, company, last_date) for company, last_date in chunk.items()]
            results = await asyncio.gather(*tasks)

        chunk_data = []
        new_dates = {}
        for company_name, latest_date, data in results:
            if not latest_date:
                latest_date = datetime.now().isoformat()
            new_dates[company_name] = latest_date
            if data:
                chunk_data.extend(data)

        return new_dates, chunk_data

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process_chunk())