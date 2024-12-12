import pandas as pd
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.stock import StockData, LatestDate, StockDataResponse
from datetime import datetime
import numpy as np

def transform_date(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    return date_obj.strftime("%Y-%m-%d")

def preprocess_data(data: pd.DataFrame):
    data['date'] = data['date'].apply(transform_date)
    data = data.sort_values(by='date')
    data = data.set_index("date")

    data.drop(['id'], axis=1, inplace=True)
    data = data.replace('', np.nan)

    data = data.dropna(subset=['closing_price'])

    columns_remove_comma = ["volume"]
    data[columns_remove_comma] = data[columns_remove_comma].apply(lambda col: col.str.replace(',', '', regex=False)).astype(float)

    columns_remove_dot = ["max_price", "min_price", "closing_price", "avg_price", "total_turnover"]
    data[columns_remove_dot] = data[columns_remove_dot].apply(lambda col: col.str.replace('.', '', regex=False))

    columns_replace_comma = ["max_price", "min_price", "closing_price", "avg_price", "total_turnover",
                             "percentage_change"]
    data[columns_replace_comma] = data[columns_replace_comma].apply(
        lambda col: col.str.replace(',', '.', regex=False)).astype(float)

    data[['max_price', 'min_price']] = data[['max_price', 'min_price']].ffill()

    return data


def get_stocks_as_dataframe(company_name: str, db: Session = next(get_db())):
    stocks = db.query(StockData).filter(StockData.company == company_name).all()

    stock_dicts = [stock.__dict__ for stock in stocks]

    for stock in stock_dicts:
        stock.pop('_sa_instance_state', None)

    df = pd.DataFrame(stock_dicts)
    return preprocess_data(df)