import pandas as pd
from sqlalchemy.orm import Session
from database.connection import get_db
from models.stocks import StockData

# Shared util library, used for both technical and lstm analysis
from preprocess.stocks_preprocess import preprocess_data

def load_stocks_as_dataframe(company_name: str, db: Session = next(get_db())):
    print(f"Querying stock data for company: {company_name}")
    try:
        stocks = db.query(StockData).filter(StockData.company == company_name).all()
        stock_dicts = [stock.__dict__ for stock in stocks]
        for stock in stock_dicts:
            stock.pop('_sa_instance_state', None)

        df = pd.DataFrame(stock_dicts)
        print(f"Found {len(stocks)} records")

        return preprocess_data(df)
    except Exception as e:
        print(f"Error querying stock data: {e}")
        return pd.DataFrame()