from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMInterface(ABC):
    """Interface for Large Language Model clients."""

    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    async def generate_structured_response(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured response following a schema."""
        pass