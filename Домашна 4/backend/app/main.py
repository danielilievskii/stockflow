from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from routers.stock_router import router as stock_router
from routers.analysis_router import router as analysis_router
from database.connection import Base, engine

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://frontend:3000",
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
app.include_router(analysis_router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Stockflow API"}