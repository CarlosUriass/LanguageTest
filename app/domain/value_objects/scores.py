from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Scores:
    """Represents language evaluation scores."""
    grammar: float
    vocabulary: float
    fluency: float

    def __post_init__(self):
        """Validate scores are within valid range."""
        for field_name, value in [("grammar", self.grammar), ("vocabulary", self.vocabulary), ("fluency", self.fluency)]:
            if not isinstance(value, (int, float)):
                raise ValueError(f"{field_name} must be a number")
            if not 0.0 <= value <= 10.0:
                raise ValueError(f"{field_name} must be between 0.0 and 10.0, got {value}")

    @property
    def average(self) -> float:
        """Calculate average score."""
        return round((self.grammar + self.vocabulary + self.fluency) / 3, 2)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            "grammar": self.grammar,
            "vocabulary": self.vocabulary,
            "fluency": self.fluency
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "Scores":
        """Create from dictionary."""
        return cls(
            grammar=data.get("grammar", 0.0),
            vocabulary=data.get("vocabulary", 0.0),
            fluency=data.get("fluency", 0.0)
        )