from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.domain.repositories.final_evaluation_repository import FinalEvaluationRepositoryInterface
from app.domain.entities.final_evaluation import FinalEvaluation
from app.infrastructure.persistence.sqlalchemy.models.final_evaluation_model import FinalEvaluationModel
from app.core.database import get_db


class SqlAlchemyFinalEvaluationRepository(FinalEvaluationRepositoryInterface):
    """SQLAlchemy implementation of final evaluation repository."""

    def __init__(self):
        self.db_session = next(get_db())

    def save(self, final_evaluation: FinalEvaluation) -> FinalEvaluation:
        """Save a final evaluation."""
        try:
            # Convert domain entity to model
            model = FinalEvaluationModel(
                user_id=final_evaluation.user_id,
                initial_level=final_evaluation.initial_level,
                final_level=final_evaluation.final_level,
                reason=final_evaluation.reason
            )
            
            self.db_session.add(model)
            self.db_session.commit()
            self.db_session.refresh(model)
            
            # Convert back to domain entity
            return FinalEvaluation(
                id=model.id,
                user_id=model.user_id,
                initial_level=model.initial_level,
                final_level=model.final_level,
                reason=model.reason,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
        except Exception as e:
            self.db_session.rollback()
            raise e
        finally:
            self.db_session.close()

    def find_by_user_id(self, user_id: int) -> Optional[FinalEvaluation]:
        """Find the most recent final evaluation by user ID."""
        try:
            model = (
                self.db_session.query(FinalEvaluationModel)
                .filter(FinalEvaluationModel.user_id == user_id)
                .order_by(desc(FinalEvaluationModel.created_at))
                .first()
            )
            
            if model:
                return FinalEvaluation(
                    id=model.id,
                    user_id=model.user_id,
                    initial_level=model.initial_level,
                    final_level=model.final_level,
                    reason=model.reason,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
            return None
        finally:
            self.db_session.close()

    def find_all_by_user_id(self, user_id: int) -> List[FinalEvaluation]:
        """Find all final evaluations by user ID."""
        try:
            models = (
                self.db_session.query(FinalEvaluationModel)
                .filter(FinalEvaluationModel.user_id == user_id)
                .order_by(desc(FinalEvaluationModel.created_at))
                .all()
            )
            
            return [
                FinalEvaluation(
                    id=model.id,
                    user_id=model.user_id,
                    initial_level=model.initial_level,
                    final_level=model.final_level,
                    reason=model.reason,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
                for model in models
            ]
        finally:
            self.db_session.close()

    def find_by_id(self, evaluation_id: int) -> Optional[FinalEvaluation]:
        """Find final evaluation by ID."""
        try:
            model = self.db_session.query(FinalEvaluationModel).filter(
                FinalEvaluationModel.id == evaluation_id
            ).first()
            
            if model:
                return FinalEvaluation(
                    id=model.id,
                    user_id=model.user_id,
                    initial_level=model.initial_level,
                    final_level=model.final_level,
                    reason=model.reason,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
            return None
        finally:
            self.db_session.close()