from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database.connection import get_db

from app.models.stock import StockData, LatestDate, StockDataResponse

router = APIRouter()

@router.get("/stocks/{company_name}", response_model=list[StockDataResponse])
def get_stocks_for_company(company_name: str, db: Session = Depends(get_db)):
    stocks = db.query(StockData).filter(StockData.company == company_name).all()
    return stocks

@router.get("/companies")
def get_stocks(db: Session = Depends(get_db)):
    companies = db.query(LatestDate).all()
    return [{"company_name": company.company_name} for company in companies]

