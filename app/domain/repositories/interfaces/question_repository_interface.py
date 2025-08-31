from abc import ABC, abstractmethod
from app.domain.entities.questions import Questions

class QuestionRepositoryInterface(ABC):
    @abstractmethod
    def list_questions(self) -> list[Questions]:
        pass