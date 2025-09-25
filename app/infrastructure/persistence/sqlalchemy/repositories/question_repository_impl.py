from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.question_repository import QuestionRepositoryInterface
from app.domain.entities.questions import Question
from app.infrastructure.persistence.sqlalchemy.models.question_model import QuestionModel
from app.core.config.database import get_db
from app.core.exceptions.evaluation_exceptions import RepositoryException


class SqlAlchemyQuestionRepository(QuestionRepositoryInterface):
    """SQLAlchemy implementation of question repository."""

    def __init__(self, db_session: Session = None):
        self.db_session = db_session

    def _get_session(self) -> Session:
        """Get database session."""
        if self.db_session:
            return self.db_session
        return next(get_db())

    def find_all(self) -> List[Question]:
        """Get all questions."""
        try:
            session = self._get_session()
            models = session.query(QuestionModel).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            raise RepositoryException(f"Failed to find all questions: {str(e)}")

    def find_by_id(self, question_id: int) -> Optional[Question]:
        """Find question by ID."""
        try:
            session = self._get_session()
            model = session.query(QuestionModel).filter(QuestionModel.id == question_id).first()
            return self._model_to_entity(model) if model else None
        except Exception as e:
            raise RepositoryException(f"Failed to find question by ID {question_id}: {str(e)}")

    def find_by_ids(self, question_ids: List[int]) -> List[Question]:
        """Find questions by multiple IDs."""
        try:
            if not question_ids:
                return []
                
            session = self._get_session()
            models = session.query(QuestionModel).filter(QuestionModel.id.in_(question_ids)).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            raise RepositoryException(f"Failed to find questions by IDs: {str(e)}")

    def create(self, question: Question) -> Question:
        """Create a new question."""
        try:
            session = self._get_session()
            model = QuestionModel(question=question.question)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise RepositoryException(f"Failed to create question: {str(e)}")

    def update(self, question: Question) -> Question:
        """Update existing question."""
        try:
            session = self._get_session()
            model = session.query(QuestionModel).filter(QuestionModel.id == question.id).first()
            if not model:
                raise RepositoryException(f"Question with ID {question.id} not found")
            
            model.question = question.question
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise RepositoryException(f"Failed to update question: {str(e)}")

    def delete(self, question_id: int) -> bool:
        """Delete question by ID."""
        try:
            session = self._get_session()
            model = session.query(QuestionModel).filter(QuestionModel.id == question_id).first()
            if not model:
                return False
            
            session.delete(model)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise RepositoryException(f"Failed to delete question: {str(e)}")

    def _model_to_entity(self, model: QuestionModel) -> Question:
        """Convert model to entity."""
        return Question(id=model.id, question=model.question)