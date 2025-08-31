from abc import ABC, abstractmethod
from app.domain.entities.evaluation import Evaluation

class EvalationRepositoryInterface(ABC):
    @abstractmethod
    def save_responses(self) -> Evaluation:
        pass