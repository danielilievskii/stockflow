import csv
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.stock import StockData
from datetime import datetime

def load_csv_to_db(csv_file_path: str):
    # Start a database session
    db: Session = SessionLocal()

    try:
        with open(csv_file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert row data to match the StockData model
                stock = StockData(
                    company=row["Company"],
                    date=datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                    closing_price=float(row["Closing Price"]),
                    max_price=float(row["Max Price"]),
                    min_price=float(row["Min Price"]),
                    avg_price=float(row["Avg Price"]),
                    percentage_change=float(row["Percentage Change"]),
                    volume=int(row["Volume"]),
                    total_turnover=float(row["Total Turnover"]),
                )
                db.add(stock)

        # Commit the transaction
        db.commit()
        print("CSV data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error loading CSV: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_csv_to_db("testdata.csv")