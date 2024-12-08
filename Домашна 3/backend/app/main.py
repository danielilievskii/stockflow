from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.stock_controller import router as stock_router
from app.crawler.data_utils import reset_all_dates_to_specific_value
from app.crawler.script import main_pipeline
from app.database.connection import Base, engine
import asyncio

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(stock_router, prefix="/api")


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    # reset_all_dates_to_specific_value("28.11.2024")
    await main_pipeline()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Stock Prediction API"}