from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Evaluation(BaseModel):
    """Domain entity for evaluations."""
    id: Optional[int] = None
    user_id: int  # Changed from str to int for consistency
    question: str
    answer: str
    estimated_level: str
    grammar: float
    vocabulary: float
    fluency: float
    mistakes: str  # JSON string
    suggestions: str  # JSON string
    created_at: Optional[datetime] = None

    def __str__(self) -> str:
        return f"Evaluation(id={self.id}, user_id={self.user_id}, level={self.estimated_level})"
