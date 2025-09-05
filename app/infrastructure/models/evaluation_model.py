from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class EvaluationModel(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    estimated_level = Column(String, nullable=False)
    grammar = Column(Float, nullable=False)
    vocabulary = Column(Float, nullable=False)
    fluency = Column(Float, nullable=False)
    mistakes = Column(String, nullable=False)
    suggestions = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
