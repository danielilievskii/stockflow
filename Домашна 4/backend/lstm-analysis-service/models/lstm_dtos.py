from pydantic import BaseModel
from typing import List

class LSTMRequestDTO(BaseModel):
    company_name: str

class Prediction(BaseModel):
    date: str
    price: float

class LSTMResponseDTO(BaseModel):
    company_name: str
    predictions: List[Prediction]