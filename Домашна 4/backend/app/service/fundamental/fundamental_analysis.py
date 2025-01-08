import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import Counter
from sqlalchemy.orm import Session
from database.connection import get_db
from models.news import CompanyNewsData


def get_company_news_as_dataframe(company_name: str, db: Session = next(get_db())) -> pd.DataFrame:

    try:
        news = (
            db.query(CompanyNewsData)
            .filter(CompanyNewsData.company == company_name)
            .filter(
                (CompanyNewsData.sentiment == None) |
                (CompanyNewsData.sentiment == "")
            )
            .all()
        )
        news_dicts = [article.__dict__ for article in news]
        for article in news_dicts:
            article.pop('_sa_instance_state', None)

        df = pd.DataFrame(news_dicts)
        print(f"Found {len(news)} news articles")

        return df
    except Exception as e:
        print(f"Error querying news data: {e}")
        return pd.DataFrame()


def analyze_sentiment(text):
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    inputs = tokenizer(
        text,
        max_length=512,
        truncation=True,
        padding="max_length",
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, axis=-1)

    finbert_label = model.config.id2label[prediction.item()]
    return finbert_label

def update_sentiment_in_dataframe(df):
    sentiments = []
    for index, row in df.iterrows():
        try:
            sentiment = analyze_sentiment(row['content'])
            sentiments.append(sentiment)
        except Exception as e:
            print(f"Error analyzing row ID {row['id']}: {e}")
            sentiments.append(None)
    df['sentiment'] = sentiments
    return df


def get_last_7_dates_sentiments(company_name: str, db: Session) -> list:
    sentiment_data = db.query(CompanyNewsData.date, CompanyNewsData.sentiment).filter(
        CompanyNewsData.company == company_name,
        CompanyNewsData.sentiment.isnot(None)
    ).order_by(CompanyNewsData.date.desc()).all()

    distinct_dates = []
    sentiments = []
    for date, sentiment in sentiment_data:
        distinct_dates.append(date)
        sentiments.append(sentiment)
        if len(distinct_dates) >= 7:
            break

    return sentiments


def predict_action(sentiments: list) -> str:
    sentiment_counts = Counter(sentiments)

    positive_count = sentiment_counts.get("positive", 0)
    negative_count = sentiment_counts.get("negative", 0)
    neutral_count = sentiment_counts.get("neutral", 0)

    if positive_count > negative_count and positive_count > neutral_count:
        return "Buy"
    elif negative_count > positive_count and negative_count > neutral_count:
        return "Sell"
    else:
        return "Hold"


def perform_fundamental_analysis(company_name):
    db_session = next(get_db())

    news_df = get_company_news_as_dataframe(company_name, db=db_session)

    news_df = update_sentiment_in_dataframe(news_df)

    for index, row in news_df.iterrows():
        db_session.query(CompanyNewsData).filter(CompanyNewsData.id == row['id']).update(
            {"sentiment": row['sentiment']}
        )
    db_session.commit()

    sentiments_last_7_dates = get_last_7_dates_sentiments(company_name, db=db_session)
    action = predict_action(sentiments_last_7_dates)

    return action