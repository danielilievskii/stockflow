import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import os
from crawler import fetch_company_data
from config import BASE_URL, HEADERS, LATEST_DATE_CSV
from data_utils import save_latest_dates_to_csv, load_latest_dates_from_csv
import multiprocessing
from multiprocessing import Pool, Manager


# Filter 1: Fetch valid companies
async def filter_1_fetch_companies():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            page_content = await response.text()
            soup = BeautifulSoup(page_content, 'html.parser')
            companies = [option.text for option in soup.select("select#Code option")
                         if not any(char.isdigit() for char in option.text)]

    print("Filter 1: Fetched companies.")
    return companies


# Filter 2: Initialize latest dates
async def filter_2_initialize_dates(companies):
    if not pd.io.common.file_exists(LATEST_DATE_CSV):
        print("Filter 2: No latest dates file found. Initializing with data for the last 10 years.")
        company_latest_dates = {company: None for company in companies}
    else:
        company_latest_dates = load_latest_dates_from_csv()
        print("Filter 2: Loaded latest dates from file.")

    return company_latest_dates


# Filter 3 - Fetch missing data in parallel
def filter_3_fetch_missing_data(company_latest_dates):
    os.makedirs('data', exist_ok=True)
    num_cores = multiprocessing.cpu_count()
    chunk_size = max(1, len(company_latest_dates) // num_cores)
    company_chunks = [{k: company_latest_dates[k] for k in list(company_latest_dates)[i:i + chunk_size]}
                      for i in range(0, len(company_latest_dates), chunk_size)]

    with Manager() as manager:
        new_dates = manager.dict()

        with Pool(num_cores) as pool:
            results = pool.map(fetch_data_for_chunk, [(chunk, new_dates) for chunk in company_chunks])

        all_latest_dates = {k: v for d in results for k, v in d.items()}
        save_latest_dates_to_csv(all_latest_dates)
        print("Filter 3: Completed fetching and updating missing data.")

def fetch_data_for_chunk(args):
    chunk, new_dates = args
    async def process_chunk():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_company_data(session, company, last_date) for company, last_date in chunk.items()]
            results = await asyncio.gather(*tasks)

            for company_name, latest_date in results:
                new_dates[company_name] = latest_date
            return new_dates

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process_chunk())