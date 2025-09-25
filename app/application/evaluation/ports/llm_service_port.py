from abc import ABC, abstractmethod
from typing import Dict, List, Any


class LLMServicePort(ABC):
    """Port for LLM service operations."""

    @abstractmethod
    async def evaluate_answers(
        self,
        questions_dict: Dict[int, str],
        answers_dict: Dict[int, str]
    ) -> Dict[str, Any]:
        """Evaluate answers using LLM and return structured feedback."""
        pass

    @abstractmethod
    async def final_evaluation(
        self,
        previous_evaluation: Dict[str, Any],
        new_answers: List[Dict[str, str]]
    ) -> str:
        """Perform final evaluation and return CEFR level."""
        pass