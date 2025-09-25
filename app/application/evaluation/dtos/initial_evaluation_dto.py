from pydantic import BaseModel, Field
from typing import List, Dict, Any


class AnswerDTO(BaseModel):
    """DTO for individual answer."""
    question_id: int = Field(..., description="ID of the question")
    answer: str = Field(..., description="User's answer")


class InitialEvaluationRequestDTO(BaseModel):
    """DTO for initial evaluation request."""
    user_id: int = Field(..., description="User ID")
    answers: List[AnswerDTO] = Field(..., description="List of answers")


class FeedbackDTO(BaseModel):
    """DTO for individual question feedback."""
    question: str
    answer: str
    estimated_level: str
    scores: Dict[str, float]
    mistakes: List[str]
    suggestions: List[str]


class InitialEvaluationResponseDTO(BaseModel):
    """DTO for initial evaluation response."""
    level: str = Field(..., description="Overall CEFR level")
    scores: Dict[str, float] = Field(..., description="Average scores")
    reason: str = Field(..., description="Explanation for the level")
    feedback: List[FeedbackDTO] = Field(..., description="Individual feedback")
    next_questions: List[str] = Field(..., description="Questions for next round")


# Backward compatibility aliases
InitialEvaluationDTO = AnswerDTO
InitialEvaluationListDTO = InitialEvaluationRequestDTO
