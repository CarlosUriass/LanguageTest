from pydantic import BaseModel
from typing import List

class FinalEvaluationDto(BaseModel):
    question: str
    answer: str

class FinalEvaluationListDTO(BaseModel):
    user_id: str
    answers: List[FinalEvaluationDto]
