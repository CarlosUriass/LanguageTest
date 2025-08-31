from sqlalchemy import Column, Integer, String  
from app.core.database import Base

class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key = True, index = True)
    question = Column(String, nullable = False)