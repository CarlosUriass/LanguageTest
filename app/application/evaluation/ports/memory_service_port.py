from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class MemoryServicePort(ABC):
    """Port for memory/cache service operations."""

    @abstractmethod
    async def save_evaluation_context(
        self,
        user_id: int,
        evaluation_data: Dict[str, Any]
    ) -> bool:
        """Save evaluation context to memory."""
        pass

    @abstractmethod
    async def get_evaluation_context(
        self,
        user_id: int
    ) -> Optional[Dict[str, Any]]:
        """Retrieve evaluation context from memory."""
        pass

    @abstractmethod
    async def clear_evaluation_context(
        self,
        user_id: int
    ) -> bool:
        """Clear evaluation context from memory."""
        pass