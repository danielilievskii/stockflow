from sqlalchemy.orm import Session
from database.connection import get_db
from models.news import CompanyNewsData
from .news_preprocess import preprocess_data
import pandas as pd

def load_news_as_dataframe(company_name: str, db: Session = next(get_db())):
    print(f"Querying stock data for company: {company_name}")
    try:
        all_news = db.query(CompanyNewsData).filter(CompanyNewsData.company == company_name).all()
        news_dicts = [news.__dict__ for news in all_news]
        for news in news_dicts:
            news.pop('_sa_instance_state', None)

        df = pd.DataFrame(news_dicts)
        print(f"Found {len(news_dicts)} news/reports")

        return preprocess_data(df, company_name, db)
    except Exception as e:
        print(f"Error querying news/reports data: {e}")
        return pd.DataFrame()