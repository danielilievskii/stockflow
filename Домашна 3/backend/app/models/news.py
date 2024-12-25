from sqlalchemy import Column, Integer, String, Date, Text
from app.database.connection import Base
from pydantic import BaseModel

class CompanyNewsData(Base):
    __tablename__ = "company_news_data"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    content = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)


class CompanyNewsLatestDate(Base):
    __tablename__ = "company_news_latest_date"

    company_name = Column(String, primary_key=True, nullable=True)
    latest_date = Column(Date, nullable=True)