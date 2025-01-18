from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Base, engine
from lstm_analysis import perform_lstm_analysis
from models.lstm_dtos import LSTMRequestDTO, LSTMResponseDTO


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
    return {"message": "Welcome to the LSTM Analysis Microservice"}

@app.post("/lstm-analysis", response_model=LSTMResponseDTO)
def lstm_analysis_post(lstm_request: LSTMRequestDTO):
    try:
        company_predictions = perform_lstm_analysis(lstm_request.company_name, 3)
        result = {
            "company_name": lstm_request.company_name,
            "predictions": [
                {"date": prediction["date"], "price": prediction["price"]}
                for prediction in company_predictions
            ]
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))