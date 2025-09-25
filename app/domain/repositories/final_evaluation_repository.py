from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.final_evaluation import FinalEvaluation


class FinalEvaluationRepositoryInterface(ABC):
    """Interface for final evaluation repository."""

    @abstractmethod
    def save(self, final_evaluation: FinalEvaluation) -> FinalEvaluation:
        """Save a final evaluation."""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[FinalEvaluation]:
        """Find the most recent final evaluation by user ID."""
        pass

    @abstractmethod
    def find_all_by_user_id(self, user_id: int) -> List[FinalEvaluation]:
        """Find all final evaluations by user ID."""
        pass

    @abstractmethod
    def find_by_id(self, evaluation_id: int) -> Optional[FinalEvaluation]:
        """Find final evaluation by ID."""
        pass