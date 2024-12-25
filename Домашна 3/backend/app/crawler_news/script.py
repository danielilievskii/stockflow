import asyncio
from app.crawler_news.filters import filter_1_fetch_companies, filter_2_initialize_dates, filter_3_fetch_missing_data
import time

async def news_pipeline():
    companies = await filter_1_fetch_companies()
    latest_dates = await filter_2_initialize_dates(companies)
    filter_3_fetch_missing_data(latest_dates)

if __name__ == "__main__":
    asyncio.run(news_pipeline())