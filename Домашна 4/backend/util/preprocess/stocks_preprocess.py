import pandas as pd
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

    data['closing_price'] = data['closing_price'].replace('', np.nan)
    data = data.dropna(subset=['closing_price'])

    if data['closing_price'].isna().all():
        return None

    data = data.replace('', 'nan')

    columns_remove_comma = ["volume"]
    data[columns_remove_comma] = data[columns_remove_comma].apply(
        lambda col: col.str.replace(',', '', regex=False)).astype(float)

    columns_remove_dot = ["max_price", "min_price", "closing_price", "avg_price", "total_turnover"]
    data[columns_remove_dot] = data[columns_remove_dot].apply(lambda col: col.str.replace('.', '', regex=False))

    columns_replace_comma = ["max_price", "min_price", "closing_price", "avg_price", "total_turnover",
                             "percentage_change"]
    data[columns_replace_comma] = data[columns_replace_comma].apply(
        lambda col: col.str.replace(',', '.', regex=False)).astype(float)

    data = data.replace('nan', np.nan)
    data['max_price'] = data.apply(lambda row: row['avg_price'] if pd.isna(row['max_price']) else row['max_price'],
                                   axis=1)
    data['min_price'] = data.apply(lambda row: row['avg_price'] if pd.isna(row['min_price']) else row['min_price'],
                                   axis=1)

    return data
