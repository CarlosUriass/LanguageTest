from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class CacheInterface(ABC):
    """Interface for cache operations."""

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        pass

    @abstractmethod
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set key-value pair with optional TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete key."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass