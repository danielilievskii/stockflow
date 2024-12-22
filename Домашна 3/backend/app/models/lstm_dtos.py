from pydantic import BaseModel

class LSTMRequestDTO(BaseModel):
    company_name: str
    #date: str

class LSTMResponseDTO(BaseModel):
    company_name: str
    date: str
    decision: str
    price: float