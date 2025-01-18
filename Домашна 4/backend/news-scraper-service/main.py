from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from script import news_pipeline
from database.connection import Base, engine

app = FastAPI()
scheduler = AsyncIOScheduler()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://backend:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start_scheduler():
    scheduler.add_job(news_pipeline, 'cron', hour=3, minute=0)
    scheduler.start()

@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    start_scheduler()

    await news_pipeline()

@app.on_event("shutdown")
async def on_shutdown():
    scheduler.shutdown()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the News Scraper API"}

@app.get("/run")
async def run_scraper(background_tasks: BackgroundTasks):
    background_tasks.add_task(news_pipeline)
    return {"message": "News scraping started in background"}