from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
from models.tech_dtos import TechAnalysisResponseDTO, TechAnalysisRequestDTO
from technical_analysis import perform_technical_analysis

app = FastAPI()

origins = [
    "http://backend:8080",
    "http://frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the LSTM Analysis API"}

@app.post("/technical-analysis", response_model=TechAnalysisResponseDTO)
def tech_analysis_post(tech_request: TechAnalysisRequestDTO):
    try:
        decision = perform_technical_analysis(tech_request.company_name, tech_request.timeframe)
        return {"company_name": tech_request.company_name, "decision": decision}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))