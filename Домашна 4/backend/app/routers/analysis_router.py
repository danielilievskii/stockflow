from fastapi import APIRouter, HTTPException
from models.tech_dtos import TechAnalysisRequestDTO, TechAnalysisResponseDTO
from models.fundamental_dtos import FundamentalRequestDTO, FundamentalResponseDTO
from models.lstm_dtos import LSTMRequestDTO, LSTMResponseDTO
import requests

router = APIRouter()

@router.post("/technical-analysis", response_model=TechAnalysisResponseDTO)
def lstm_analysis(tech_request: TechAnalysisRequestDTO):
    try:
        response = requests.post(
            "http://technical-analysis-service:8080/technical-analysis",
            json={
                "company_name": tech_request.company_name,
                "timeframe": tech_request.timeframe
            },
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            return response.json()

        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fundamental-analysis", response_model=FundamentalResponseDTO)
def lstm_analysis(fundamental_reqeust: FundamentalRequestDTO):
    try:
        response = requests.post(
            "http://fundamental-analysis-service:8080/fundamental-analysis",
            json={"company_name": fundamental_reqeust.company_name},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            return response.json()

        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lstm-analysis", response_model=LSTMResponseDTO)
def lstm_analysis(lstm_request: LSTMRequestDTO):
    try:
        response = requests.post(
            "http://lstm-analysis-service:8080/lstm-analysis",
            json={"company_name": lstm_request.company_name},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            return response.json()

        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))