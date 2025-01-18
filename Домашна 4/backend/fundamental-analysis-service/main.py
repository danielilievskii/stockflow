from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
from fundamental_analysis import perform_fundamental_analysis
from models.fundamental_dtos import FundamentalRequestDTO, FundamentalResponseDTO


app = FastAPI()

origins = [
    "http://backend:8080",
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
    return {"message": "Welcome to the Fundamental Analysis Microservice"}

@app.post("/fundamental-analysis", response_model=FundamentalResponseDTO)
def tech_analysis_post(fundamental_request: FundamentalRequestDTO):
    try:
        decision = perform_fundamental_analysis(fundamental_request.company_name)
        return {"company_name": fundamental_request.company_name, "decision": decision}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#