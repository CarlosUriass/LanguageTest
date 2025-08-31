from app.domain.entities.questions import Questions
from app.domain.repositories.interfaces.question_repository_interface import QuestionRepositoryInterface
from app.infrastructure.models.question_model import QuestionModel
from app.core.database import SessionLocal

class QuestionRepository(QuestionRepositoryInterface):
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def list_questions(self) -> list[Questions]:
        questions = self.db.query(QuestionModel).all()
        return [Questions(id=q.id, question=q.question) for q in questions]

    def get_questions_by_ids(self, question_ids: list[int]) -> list[Questions]:
        questions = self.db.query(QuestionModel).filter(QuestionModel.id.in_(question_ids)).all()
        return [Questions(id=q.id, question=q.question) for q in questions]
