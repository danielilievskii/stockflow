from sqlalchemy import Column, Integer, String
from database.connection import Base

class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=True)
    date = Column(String, nullable=True)
    closing_price = Column(String, nullable=True)
    max_price = Column(String, nullable=True)
    min_price = Column(String, nullable=True)
    avg_price = Column(String, nullable=True)
    percentage_change = Column(String, nullable=True)
    volume = Column(String, nullable=True)
    total_turnover = Column(String, nullable=True)

    class Config:
        from_attributes = True

class LatestDate(Base):
    __tablename__ = "latest_date"

    company_name = Column(String, primary_key=True, nullable=False)
    latest_date = Column(String, nullable=False)