from fastapi import APIRouter, HTTPException
from app.models.tech_dtos import TechAnalysisRequestDTO, TechAnalysisResponseDTO
from app.models.fundamental_dtos import FundamentalRequestDTO, FundamentalResponseDTO
from app.models.lstm_dtos import LSTMRequestDTO, LSTMResponseDTO

from app.service.technical.technicalAnalysis import perform_technical_analysis
from app.service.fundamental.fundamentalAnalysis import perform_fundamental_analysis
from app.service.lstm.lstm_prediction import perform_lstm_analysis

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
        decision = perform_fundamental_analysis(fundamental_request.company_name)
        return {"company_name": fundamental_request.company_name, "decision": decision}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lstm-analysis", response_model=LSTMResponseDTO)
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