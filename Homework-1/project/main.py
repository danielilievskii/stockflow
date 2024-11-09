import asyncio
from filters import filter_1_fetch_companies, filter_2_initialize_dates, filter_3_fetch_missing_data
import time

async def main_pipeline():
    start_time = time.time()

    companies = await filter_1_fetch_companies()
    latest_dates = await filter_2_initialize_dates(companies)
    await filter_3_fetch_missing_data(latest_dates)

    end_time = time.time()
    print(f"Pipeline completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main_pipeline())