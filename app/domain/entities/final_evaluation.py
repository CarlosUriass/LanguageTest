from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class FinalEvaluation:
    """Domain entity representing a final evaluation result."""
    
    user_id: int
    final_level: str
    initial_level: Optional[str] = None
    reason: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate the final evaluation data."""
        valid_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        
        if self.final_level not in valid_levels:
            raise ValueError(f"Invalid final level: {self.final_level}. Must be one of {valid_levels}")
        
        if self.initial_level and self.initial_level not in valid_levels:
            raise ValueError(f"Invalid initial level: {self.initial_level}. Must be one of {valid_levels}")
            
        if self.user_id <= 0:
            raise ValueError("User ID must be positive")