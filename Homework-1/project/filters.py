import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
import os
from crawler import fetch_company_data
from config import BASE_URL, HEADERS, LATEST_DATE_CSV
from data_utils import save_latest_dates_to_csv, load_latest_dates_from_csv


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


# Filter 3: Fetch missing data from last known date to today
async def filter_3_fetch_missing_data(company_latest_dates):
    print("Filter 3: Checking for missing data.")
    os.makedirs('data', exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_company_data(session, company, last_date) for company, last_date in company_latest_dates.items()]
        results = await asyncio.gather(*tasks)

        new_company_latest_dates = {company_name: latest_date for company_name, latest_date in results}
        save_latest_dates_to_csv(new_company_latest_dates)

    print("Filter 3: Completed fetching and updating missing data.")