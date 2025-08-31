from pydantic import BaseModel

class QuestionDTO(BaseModel):
    question_text: str