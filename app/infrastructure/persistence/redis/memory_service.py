import json
import redis
from typing import Dict, Any, Optional

from app.application.evaluation.ports.memory_service_port import MemoryServicePort
from app.core.config.settings import settings
from app.core.exceptions.evaluation_exceptions import CacheException


class RedisMemoryService(MemoryServicePort):
    """Redis implementation of memory service."""

    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
        except Exception as e:
            raise CacheException(f"Failed to connect to Redis: {str(e)}")

    async def save_evaluation_context(
        self,
        user_id: int,
        evaluation_data: Dict[str, Any]
    ) -> bool:
        """Save evaluation context to Redis."""
        try:
            key = self._get_evaluation_key(user_id)
            serialized_data = json.dumps(evaluation_data)
            
            # Set with 24 hour expiration (86400 seconds)
            result = self.redis_client.setex(key, 86400, serialized_data)
            return bool(result)
            
        except Exception as e:
            raise CacheException(f"Failed to save evaluation context: {str(e)}")

    async def get_evaluation_context(
        self,
        user_id: int
    ) -> Optional[Dict[str, Any]]:
        """Retrieve evaluation context from Redis."""
        try:
            key = self._get_evaluation_key(user_id)
            data = self.redis_client.get(key)
            
            if data is None:
                return None
                
            return json.loads(data)
            
        except json.JSONDecodeError as e:
            raise CacheException(f"Failed to parse evaluation context: {str(e)}")
        except Exception as e:
            raise CacheException(f"Failed to retrieve evaluation context: {str(e)}")

    async def clear_evaluation_context(
        self,
        user_id: int
    ) -> bool:
        """Clear evaluation context from Redis."""
        try:
            key = self._get_evaluation_key(user_id)
            result = self.redis_client.delete(key)
            return bool(result)
            
        except Exception as e:
            raise CacheException(f"Failed to clear evaluation context: {str(e)}")

    def _get_evaluation_key(self, user_id: int) -> str:
        """Generate Redis key for evaluation context."""
        return f"evaluation:user:{user_id}"