from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.questions import Question


class QuestionRepositoryInterface(ABC):
    """Interface for question repository operations."""

    @abstractmethod
    def find_all(self) -> List[Question]:
        """Get all questions."""
        pass

    @abstractmethod
    def find_by_id(self, question_id: int) -> Optional[Question]:
        """Find question by ID."""
        pass

    @abstractmethod
    def find_by_ids(self, question_ids: List[int]) -> List[Question]:
        """Find questions by multiple IDs."""
        pass

    @abstractmethod
    def create(self, question: Question) -> Question:
        """Create a new question."""
        pass

    @abstractmethod
    def update(self, question: Question) -> Question:
        """Update existing question."""
        pass

    @abstractmethod
    def delete(self, question_id: int) -> bool:
        """Delete question by ID."""
        pass