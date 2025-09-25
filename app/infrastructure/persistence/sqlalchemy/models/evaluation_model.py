from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.config.database import Base


class EvaluationModel(Base):
    """SQLAlchemy model for evaluations."""
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    estimated_level = Column(String, nullable=False)
    grammar = Column(Float, nullable=False)
    vocabulary = Column(Float, nullable=False)
    fluency = Column(Float, nullable=False)
    mistakes = Column(String, nullable=False)  # JSON string
    suggestions = Column(String, nullable=False)  # JSON string
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<EvaluationModel(id={self.id}, user_id={self.user_id}, level={self.estimated_level})>"