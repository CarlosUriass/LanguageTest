import json
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.evaluation_repository import EvaluationRepositoryInterface
from app.domain.entities.evaluation import Evaluation
from app.infrastructure.persistence.sqlalchemy.models.evaluation_model import EvaluationModel
from app.core.config.database import get_db
from app.core.exceptions.evaluation_exceptions import RepositoryException


class SqlAlchemyEvaluationRepository(EvaluationRepositoryInterface):
    """SQLAlchemy implementation of evaluation repository."""

    def __init__(self, db_session: Session = None):
        self.db_session = db_session

    def _get_session(self) -> Session:
        """Get database session."""
        if self.db_session:
            return self.db_session
        return next(get_db())

    def save(self, evaluation: Evaluation) -> Evaluation:
        """Save evaluation to repository."""
        try:
            session = self._get_session()
            model = EvaluationModel(
                user_id=evaluation.user_id,
                question=evaluation.question,
                answer=evaluation.answer,
                estimated_level=evaluation.estimated_level,
                grammar=evaluation.grammar,
                vocabulary=evaluation.vocabulary,
                fluency=evaluation.fluency,
                mistakes=evaluation.mistakes,
                suggestions=evaluation.suggestions
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise RepositoryException(f"Failed to save evaluation: {str(e)}")

    def find_by_user_id(self, user_id: int) -> List[Evaluation]:
        """Find evaluations by user ID."""
        try:
            session = self._get_session()
            models = session.query(EvaluationModel).filter(EvaluationModel.user_id == user_id).all()
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            raise RepositoryException(f"Failed to find evaluations for user {user_id}: {str(e)}")

    def find_by_id(self, evaluation_id: int) -> Optional[Evaluation]:
        """Find evaluation by ID."""
        try:
            session = self._get_session()
            model = session.query(EvaluationModel).filter(EvaluationModel.id == evaluation_id).first()
            return self._model_to_entity(model) if model else None
        except Exception as e:
            raise RepositoryException(f"Failed to find evaluation by ID {evaluation_id}: {str(e)}")

    def update(self, evaluation: Evaluation) -> Evaluation:
        """Update existing evaluation."""
        try:
            session = self._get_session()
            model = session.query(EvaluationModel).filter(EvaluationModel.id == evaluation.id).first()
            if not model:
                raise RepositoryException(f"Evaluation with ID {evaluation.id} not found")
            
            model.question = evaluation.question
            model.answer = evaluation.answer
            model.estimated_level = evaluation.estimated_level
            model.grammar = evaluation.grammar
            model.vocabulary = evaluation.vocabulary
            model.fluency = evaluation.fluency
            model.mistakes = evaluation.mistakes
            model.suggestions = evaluation.suggestions
            
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            session.rollback()
            raise RepositoryException(f"Failed to update evaluation: {str(e)}")

    def delete(self, evaluation_id: int) -> bool:
        """Delete evaluation by ID."""
        try:
            session = self._get_session()
            model = session.query(EvaluationModel).filter(EvaluationModel.id == evaluation_id).first()
            if not model:
                return False
            
            session.delete(model)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise RepositoryException(f"Failed to delete evaluation: {str(e)}")

    def _model_to_entity(self, model: EvaluationModel) -> Evaluation:
        """Convert model to entity."""
        return Evaluation(
            id=model.id,
            user_id=model.user_id,
            question=model.question,
            answer=model.answer,
            estimated_level=model.estimated_level,
            grammar=model.grammar,
            vocabulary=model.vocabulary,
            fluency=model.fluency,
            mistakes=model.mistakes,
            suggestions=model.suggestions,
            created_at=model.created_at
        )