from typing import List
from app.application.questions.dtos.questions_dto import QuestionListResponseDTO, QuestionDTO
from app.domain.repositories.question_repository import QuestionRepositoryInterface
from app.core.exceptions.evaluation_exceptions import RepositoryException


class ListQuestionsUseCase:
    """Use case for listing all available questions."""

    def __init__(self, question_repository: QuestionRepositoryInterface):
        self.question_repository = question_repository

    def execute(self) -> QuestionListResponseDTO:
        """Execute the list questions use case."""
        try:
            # Get all questions from repository
            questions = self.question_repository.find_all()
            
            # Convert to DTOs
            question_dtos = [
                QuestionDTO(
                    id=question.id,
                    question=question.question
                )
                for question in questions
            ]
            
            return QuestionListResponseDTO(questions=question_dtos)
            
        except Exception as e:
            raise RepositoryException(f"Failed to retrieve questions: {str(e)}")