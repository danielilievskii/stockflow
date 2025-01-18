from pydantic import BaseModel

class FundamentalRequestDTO(BaseModel):
    company_name: str

class FundamentalResponseDTO(BaseModel):
    company_name: str
    decision: str