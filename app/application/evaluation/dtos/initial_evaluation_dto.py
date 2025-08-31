from pydantic import BaseModel
from typing import List

class InitialEvaluationDTO(BaseModel):
    question_id: int
    answer: str

class InitialEvaluationListDTO(BaseModel):
    user_id: str  
    answers: List[InitialEvaluationDTO]
