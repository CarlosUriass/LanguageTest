import json
from typing import Dict, List

from app.application.evaluation.dtos.initial_evaluation_dto import (
    InitialEvaluationRequestDTO,
    InitialEvaluationResponseDTO,
    FeedbackDTO
)
from app.application.evaluation.ports.llm_service_port import LLMServicePort
from app.application.evaluation.ports.memory_service_port import MemoryServicePort
from app.domain.repositories.question_repository import QuestionRepositoryInterface
from app.domain.repositories.evaluation_repository import EvaluationRepositoryInterface
from app.domain.entities.evaluation import Evaluation
from app.domain.services.level_calculator import LevelCalculatorService
from app.domain.value_objects.scores import Scores
from app.core.exceptions.evaluation_exceptions import EvaluationException


class InitialEvaluationUseCase:
    """Use case for handling initial evaluation of user answers."""

    def __init__(
        self,
        llm_service: LLMServicePort,
        memory_service: MemoryServicePort,
        question_repository: QuestionRepositoryInterface,
        evaluation_repository: EvaluationRepositoryInterface,
        level_calculator: LevelCalculatorService
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.question_repository = question_repository
        self.evaluation_repository = evaluation_repository
        self.level_calculator = level_calculator

    async def execute(self, request: InitialEvaluationRequestDTO) -> InitialEvaluationResponseDTO:
        """Execute initial evaluation use case."""
        try:
            # 1. Get questions from repository
            question_ids = [answer.question_id for answer in request.answers]
            questions = self.question_repository.find_by_ids(question_ids)
            
            if len(questions) != len(question_ids):
                raise EvaluationException("Some questions not found")

            # 2. Prepare data for LLM
            questions_dict = {q.id: q.question for q in questions}
            answers_dict = {answer.question_id: answer.answer for answer in request.answers}

            # 3. Get LLM evaluation
            llm_response = await self.llm_service.evaluate_answers(questions_dict, answers_dict)

            # 4. Process LLM response
            feedback_list = []
            individual_levels = []
            individual_scores = []

            for feedback_data in llm_response["feedback"]:
                feedback = FeedbackDTO(
                    question=feedback_data["question"],
                    answer=feedback_data["answer"],
                    estimated_level=feedback_data["estimated_level"],
                    scores=feedback_data["scores"],
                    mistakes=feedback_data["mistakes"],
                    suggestions=feedback_data["suggestions"]
                )
                feedback_list.append(feedback)
                individual_levels.append(feedback_data["estimated_level"])
                individual_scores.append(Scores.from_dict(feedback_data["scores"]))

            # 5. Calculate overall level and scores using domain service
            overall_level = self.level_calculator.calculate_overall_level(individual_levels)
            average_scores = self.level_calculator.calculate_average_scores(individual_scores)

            # 6. Create response DTO
            response = InitialEvaluationResponseDTO(
                level=overall_level,
                scores=average_scores.to_dict(),
                reason=llm_response.get("reason", "Based on overall performance"),
                feedback=feedback_list,
                next_questions=llm_response.get("next_questions", [])
            )

            # 7. Save to memory for later use
            await self.memory_service.save_evaluation_context(
                request.user_id,
                response.dict()
            )

            # 8. Save evaluations to repository
            for feedback in feedback_list:
                evaluation = Evaluation(
                    user_id=request.user_id,
                    question=feedback.question,
                    answer=feedback.answer,
                    estimated_level=feedback.estimated_level,
                    grammar=feedback.scores["grammar"],
                    vocabulary=feedback.scores["vocabulary"],
                    fluency=feedback.scores["fluency"],
                    mistakes=json.dumps(feedback.mistakes),
                    suggestions=json.dumps(feedback.suggestions)
                )
                self.evaluation_repository.save(evaluation)

            return response

        except Exception as e:
            raise EvaluationException(f"Failed to process initial evaluation: {str(e)}")