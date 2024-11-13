import pandas as pd
from config import LATEST_DATE_CSV

def save_latest_dates_to_csv(company_latest_dates):
    latest_dates_df = pd.DataFrame(list(company_latest_dates.items()), columns=["Company Name", "Latest Date"])
    latest_dates_df.to_csv(LATEST_DATE_CSV, index=False)

def load_latest_dates_from_csv():
    if pd.io.common.file_exists(LATEST_DATE_CSV):
        latest_dates_df = pd.read_csv(LATEST_DATE_CSV)
        return {row["Company Name"]: row["Latest Date"] for _, row in latest_dates_df.iterrows()}
    return None

def append_data_to_csv(data, csv_file_path):
    data_df = pd.DataFrame(data)
    data_df.to_csv(csv_file_path, mode='a', header=False, index=False)


def create_csv(csv_file_path):
    headers = [
        "Company",
        "Date",
        "Closing Price",
        "Max Price",
        "Min Price",
        "Avg Price",
        "Percentage Change",
        "Volume",
        "Total Turnover"
    ]
    empty_df = pd.DataFrame(columns=headers)
    empty_df.to_csv(csv_file_path, index=False)