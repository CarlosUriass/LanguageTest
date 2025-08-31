from app.domain.entities.evaluation import Evaluation
from app.domain.repositories.interfaces.evaluation_repository_interface import EvalationRepositoryInterface
from app.infrastructure.models.evaluation_model import EvaluationModel
from app.core.database import SessionLocal

class EvaluationRepository(EvalationRepositoryInterface):
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def save_responses(self, responses: Evaluation):
        evaluation = EvaluationModel(
            user_id=responses.user_id,
            question=responses.question,
            answer=responses.answer,
            estimated_level=responses.estimated_level,
            grammar=responses.grammar,
            vocabulary=responses.vocabulary,
            fluency=responses.fluency,
            mistakes=responses.mistakes,
            suggestions=responses.suggestions,
        )

        self.db.add(evaluation)
        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation
