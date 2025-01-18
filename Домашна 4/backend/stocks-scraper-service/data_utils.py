
from database.connection import SessionLocal
from models.stock_data import StockData, LatestDate
def save_latest_dates_to_db(company_latest_dates: dict):
    with SessionLocal() as db:
        for company_name, latest_date in company_latest_dates.items():
            existing_entry = db.query(LatestDate).filter(LatestDate.company_name == company_name).first()

            if existing_entry:
                existing_entry.latest_date = latest_date
            else:
                db.add(LatestDate(company_name=company_name, latest_date=latest_date))

        db.commit()

    print("Stock Data Crawler - Filter 3: Latest dates were saved to the database.")

def load_latest_dates_from_db() -> dict:
    with SessionLocal() as db:
        latest_dates = db.query(LatestDate).all()
        return {latest_date.company_name: latest_date.latest_date for latest_date in latest_dates}

def append_data_to_db(data: list):
    with SessionLocal() as db:
        for entry in data:
            db.add(StockData(**entry))
        db.commit()
    print("Stock Data Crawler - Filter 3: Stock Data was appended to the database.")

def update_latest_dates_to(date_value: str):
    with SessionLocal() as db:
        db.query(LatestDate).update({LatestDate.latest_date: date_value})
        db.commit()
    print(f"All latest dates have been updated to {date_value}.")

