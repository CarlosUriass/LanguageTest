from pydantic import BaseModel
from typing import Optional


class Question(BaseModel):
    """Domain entity for questions."""
    id: Optional[int] = None
    question: str

    def __str__(self) -> str:
        return f"Question(id={self.id}, question='{self.question[:50]}...')"