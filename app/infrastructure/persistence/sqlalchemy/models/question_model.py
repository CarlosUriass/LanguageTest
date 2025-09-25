from sqlalchemy import Column, Integer, String
from app.core.config.database import Base


class QuestionModel(Base):
    """SQLAlchemy model for questions."""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<QuestionModel(id={self.id}, question='{self.question[:50]}...')>"