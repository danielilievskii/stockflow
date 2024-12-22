from fastapi import APIRouter, HTTPException
from app.models.tech_dtos import TechAnalysisRequestDTO, TechAnalysisResponseDTO
from app.models.fundamental_dtos import FundamentalRequestDTO, FundamentalResponseDTO
from app.models.lstm_dtos import LSTMRequestDTO, LSTMResponseDTO

from app.service.technical.technicalAnalysis import perform_technical_analysis

router = APIRouter()

@router.post("/technical-analysis", response_model=TechAnalysisResponseDTO)
def tech_analysis_post(tech_request: TechAnalysisRequestDTO):
    try:
        decision = perform_technical_analysis(tech_request.company_name, tech_request.timeframe)
        return {"company_name": tech_request.company_name, "decision": decision}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fundamental-analysis", response_model=FundamentalResponseDTO)
def tech_analysis_post(fundamental_request: FundamentalRequestDTO):
    try:
        # Default values for testing purposes
        return {"company_name": fundamental_request.company_name, "decision": "Buy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lstm-analysis", response_model=LSTMResponseDTO)
def lstm_analysis_post(lstm_request: LSTMRequestDTO):
    try:
        # Default values for testing purposes
        return {"company_name": lstm_request.company_name, "date": lstm_request.date, "decision": "Buy", "price": 3000}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))