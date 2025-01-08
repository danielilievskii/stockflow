
from database.connection import SessionLocal
from models.stock import StockData, LatestDate
from models.news import CompanyNewsLatestDate, CompanyNewsData


def save_latest_dates_to_db(company_latest_dates: dict):
    with SessionLocal() as db:
        for company_name, latest_date in company_latest_dates.items():
            # Check if the company already exists
            existing_entry = db.query(CompanyNewsLatestDate).filter(CompanyNewsLatestDate.company_name == company_name).first()

            if existing_entry:
                # Update the existing record
                existing_entry.latest_date = latest_date
            else:
                # Insert a new record
                db.add(CompanyNewsLatestDate(company_name=company_name, latest_date=latest_date))

        db.commit()

    print("News Crawler - Filter 3: Latest dates were saved to the database.")

def load_latest_dates_from_db() -> dict:
    with SessionLocal() as db:
        latest_dates = db.query(CompanyNewsLatestDate).all()
        return {latest_date.company_name: latest_date.latest_date for latest_date in latest_dates}

def append_data_to_db(data: list):
    with SessionLocal() as db:
        for entry in data:
            db.add(CompanyNewsData(**entry))
        db.commit()
    print("News Crawler - Filter 3: News were appended to the database.")

def reset_all_dates_to_specific_value(date_value: str):
    with SessionLocal() as db:
        db.query(CompanyNewsLatestDate).update({CompanyNewsLatestDate.latest_date: date_value})
        db.commit()
    print(f"All dates in 'latest_date' table have been updated to {date_value}.")

