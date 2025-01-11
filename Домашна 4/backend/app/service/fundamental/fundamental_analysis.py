import torch
import pandas as pd
from collections import Counter
from sqlalchemy.orm import Session
from database.connection import get_db
from models.news import CompanyNewsData
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from service.preprocess.news_preprocess import get_news_as_dataframe

FINBERT_MODEL_NAME = "ProsusAI/finbert"


def initialize_sentiment_model():
    tokenizer = AutoTokenizer.from_pretrained(FINBERT_MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(FINBERT_MODEL_NAME)
    return tokenizer, model


def analyze_sentiment(text, tokenizer, model):
    inputs = tokenizer(
        text,
        max_length=512,
        truncation=True,
        padding="max_length",
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, axis=-1)
    return model.config.id2label[prediction.item()]


def update_sentiment_in_dataframe(df, tokenizer, model):
    sentiments = []
    for index, row in df.iterrows():
        try:
            if pd.isna(row['sentiment']) or row['sentiment'] == "":
                sentiment = analyze_sentiment(row['content'], tokenizer, model)
                sentiments.append(sentiment)
            else:
                sentiments.append(row['sentiment'])
        except Exception as e:
            print(f"Error analyzing row ID {row['id']}: {e}")
            sentiments.append(None)
    df['sentiment'] = sentiments
    return df


def update_database_with_sentiments(news_df, db: Session = next(get_db())):
    for index, row in news_df.iterrows():
        db.query(CompanyNewsData).filter(CompanyNewsData.id == row['id']).update(
            {"sentiment": row['sentiment']}
        )
    db.commit()


def get_last_sentiments(news_df, days=7):
    sorted_news_df = news_df.sort_values(by='date', ascending=False)
    last_days = sorted_news_df.head(days)
    sentiments = last_days['sentiment'].tolist()
    return sentiments


def predict_action_from_sentiments(sentiments):
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
    tokenizer, model = initialize_sentiment_model()

    news_df = get_news_as_dataframe(company_name)
    news_df = update_sentiment_in_dataframe(news_df, tokenizer, model)

    update_database_with_sentiments(news_df)

    last_sentiments = get_last_sentiments(news_df)
    recommended_action = predict_action_from_sentiments(last_sentiments)

    return recommended_action
