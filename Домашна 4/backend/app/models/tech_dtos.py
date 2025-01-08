from pydantic import BaseModel

class TechAnalysisRequestDTO(BaseModel):
    company_name: str
    timeframe: int

class TechAnalysisResponseDTO(BaseModel):
    company_name: str
    decision: str