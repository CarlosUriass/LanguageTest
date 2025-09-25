from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.evaluation import Evaluation


class EvaluationRepositoryInterface(ABC):
    """Interface for evaluation repository operations."""

    @abstractmethod
    def save(self, evaluation: Evaluation) -> Evaluation:
        """Save evaluation to repository."""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Evaluation]:
        """Find evaluations by user ID."""
        pass

    @abstractmethod
    def find_by_id(self, evaluation_id: int) -> Optional[Evaluation]:
        """Find evaluation by ID."""
        pass

    @abstractmethod
    def update(self, evaluation: Evaluation) -> Evaluation:
        """Update existing evaluation."""
        pass

    @abstractmethod
    def delete(self, evaluation_id: int) -> bool:
        """Delete evaluation by ID."""
        pass