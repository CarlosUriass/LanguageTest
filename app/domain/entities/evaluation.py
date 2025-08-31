from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Evaluation(BaseModel):
    id: Optional[int] = None
    user_id: str
    question: str
    answer: str
    estimated_level: str
    grammar: float
    vocabulary: float
    fluency: float
    mistakes: str
    suggestions: str
    created_at: Optional[datetime] = None
