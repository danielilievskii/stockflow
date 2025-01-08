import pandas as pd
from sqlalchemy.orm import Session
from database.connection import get_db
from models.news import CompanyNewsData

from googletrans import Translator

translator = Translator()
def preprocess_data(data: pd.DataFrame, company_name, db):
    cyrillic_data = data[data['content'].str.contains('[а-шА-Ш]', regex=True)]
    cyrillic_ids = cyrillic_data['id'].tolist()

    data = data[~data['content'].str.contains('[а-шА-Ш]', regex=True)]

    data = data.sort_values(by='date')
    data = data.set_index("date")

    # Remove corrupted data in database
    if cyrillic_ids:
        db.query(CompanyNewsData).filter(
            CompanyNewsData.company == company_name,
            CompanyNewsData.id.in_(cyrillic_ids)
        ).delete(synchronize_session=False)
        db.commit()

    return data

def get_news_as_dataframe(company_name: str, db: Session = next(get_db())):
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
