from app.application.evaluation.dtos.final_evaluation_dto import (
    FinalEvaluationRequestDTO,
    FinalEvaluationResponseDTO
)
from app.application.evaluation.ports.llm_service_port import LLMServicePort
from app.application.evaluation.ports.memory_service_port import MemoryServicePort
from app.domain.services.level_calculator import LevelCalculatorService
from app.domain.repositories.final_evaluation_repository import FinalEvaluationRepositoryInterface
from app.domain.entities.final_evaluation import FinalEvaluation
from app.core.exceptions.evaluation_exceptions import (
    EvaluationException,
    EvaluationNotFoundException
)


class FinalEvaluationUseCase:
    """Use case for handling final evaluation and level determination."""

    def __init__(
        self,
        llm_service: LLMServicePort,
        memory_service: MemoryServicePort,
        level_calculator: LevelCalculatorService,
        final_evaluation_repository: FinalEvaluationRepositoryInterface
    ):
        self.llm_service = llm_service
        self.memory_service = memory_service
        self.level_calculator = level_calculator
        self.final_evaluation_repository = final_evaluation_repository

    async def execute(self, request: FinalEvaluationRequestDTO) -> FinalEvaluationResponseDTO:
        """Execute final evaluation use case."""
        try:
            # 1. Get previous evaluation context from memory
            previous_evaluation = await self.memory_service.get_evaluation_context(request.user_id)
            
            if not previous_evaluation:
                raise EvaluationNotFoundException(
                    f"No initial evaluation found for user {request.user_id}"
                )

            # 2. Prepare new answers with questions from previous evaluation
            new_answers_with_questions = []
            next_questions = previous_evaluation.get("next_questions", [])
            
            for idx, answer in enumerate(request.answers):
                question_text = (
                    next_questions[idx] if idx < len(next_questions) 
                    else f"Question {idx + 1}"
                )
                new_answers_with_questions.append({
                    "question": question_text,
                    "answer": answer.answer
                })

            # 3. Get final evaluation from LLM
            llm_result = await self.llm_service.final_evaluation(
                previous_evaluation,
                new_answers_with_questions
            )

            # Extract final level and reason
            if isinstance(llm_result, str):
                final_level = llm_result.strip()
                reason = "Final level determined based on comprehensive analysis"
            else:
                final_level = llm_result.get("final_level", "").strip()
                reason = llm_result.get("reason", "Final level determined based on comprehensive analysis")

            # 4. Validate level progression (optional business rule)
            previous_level = previous_evaluation.get("level", "A1")
            if not self.level_calculator.validate_level_progression(previous_level, final_level):
                # Log warning but don't fail - LLM decision takes precedence
                pass

            # 5. Save final evaluation to repository
            final_evaluation_entity = FinalEvaluation(
                user_id=request.user_id,
                initial_level=previous_level,
                final_level=final_level,
                reason=reason
            )
            saved_evaluation = self.final_evaluation_repository.save(final_evaluation_entity)

            # 6. Clear evaluation context from memory (cleanup)
            await self.memory_service.clear_evaluation_context(request.user_id)

            # 7. Return final result
            return FinalEvaluationResponseDTO(
                final_level=final_level,
                reason=reason
            )

        except EvaluationNotFoundException:
            raise
        except Exception as e:
            raise EvaluationException(f"Failed to process final evaluation: {str(e)}")