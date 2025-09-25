from enum import Enum
from typing import List


class CEFRLevel(Enum):
    """Common European Framework of Reference for Languages levels."""
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

    @classmethod
    def get_all_levels(cls) -> List[str]:
        """Get all CEFR levels as strings."""
        return [level.value for level in cls]

    @classmethod
    def is_valid_level(cls, level: str) -> bool:
        """Check if a level string is valid."""
        return level in cls.get_all_levels()

    def __str__(self) -> str:
        return self.value