from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.application.questions.use_cases.list_questions_use_case import ListQuestionsUseCase
from app.application.questions.dtos.questions_dto import QuestionListResponseDTO
from app.presentation.api.dependencies import get_list_questions_use_case
from app.core.exceptions.evaluation_exceptions import RepositoryException

router = APIRouter(tags=["questions"])


@router.get("/", response_model=QuestionListResponseDTO)
async def list_questions(
    use_case: ListQuestionsUseCase = Depends(get_list_questions_use_case)
) -> QuestionListResponseDTO:
    """
    Get all available questions for evaluation.
    
    Returns a list of questions that users can answer for language evaluation.
    """
    try:
        return use_case.execute()
    except RepositoryException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")