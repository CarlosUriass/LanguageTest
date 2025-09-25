from pydantic import BaseModel, Field
from typing import List


class QuestionDTO(BaseModel):
    """DTO for individual question."""
    id: int = Field(..., description="Question ID")
    question: str = Field(..., description="Question text")


class QuestionListResponseDTO(BaseModel):
    """DTO for list of questions response."""
    questions: List[QuestionDTO] = Field(..., description="List of available questions")