from pydantic import BaseModel, Field
from typing import List


class FinalAnswerDTO(BaseModel):
    """DTO for final evaluation answer."""
    answer: str = Field(..., description="User's answer to follow-up question")


class FinalEvaluationRequestDTO(BaseModel):
    """DTO for final evaluation request."""
    user_id: int = Field(..., description="User ID")
    answers: List[FinalAnswerDTO] = Field(..., description="List of final answers")


class FinalEvaluationResponseDTO(BaseModel):
    """DTO for final evaluation response."""
    final_level: str = Field(..., description="Final CEFR level determination")
    reason: str = Field(..., description="Explanation for the final level")


# Backward compatibility aliases
FinalEvaluationDto = FinalAnswerDTO
FinalEvaluationListDTO = FinalEvaluationRequestDTO
