from fastapi.encoders import jsonable_encoder
from app.application.evaluation.dtos.initial_evaluation_dto import InitialEvaluationDTO
from app.application.evaluation.services.evaluation_service import EvaluationService
from app.infrastructure.repositories.evaluation_repository import EvaluationRepository

class EvaluationController:
    def __init__(self, repo: EvaluationRepository, service: EvaluationService):
        self.repo = repo
        self.service = service

    def evaluate(self, answers: InitialEvaluationDTO):
        result = self.service.evaluate_answers(answers)

        return jsonable_encoder(result)
