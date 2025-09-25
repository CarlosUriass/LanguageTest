from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.config.database import Base


class FinalEvaluationModel(Base):
    """SQLAlchemy model for final evaluations."""
    __tablename__ = "final_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    initial_level = Column(String(10), nullable=True)  # Nivel de la evaluación inicial
    final_level = Column(String(10), nullable=False)   # Nivel final determinado
    reason = Column(Text, nullable=True)               # Razón del LLM para el nivel final
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<FinalEvaluationModel(user_id={self.user_id}, final_level='{self.final_level}')>"