from fastapi import APIRouter, Depends, HTTPException

from app.application.evaluation.use_cases.initial_evaluation_use_case import InitialEvaluationUseCase
from app.application.evaluation.use_cases.final_evaluation_use_case import FinalEvaluationUseCase
from app.application.evaluation.dtos.initial_evaluation_dto import (
    InitialEvaluationRequestDTO,
    InitialEvaluationResponseDTO
)
from app.application.evaluation.dtos.final_evaluation_dto import (
    FinalEvaluationRequestDTO,
    FinalEvaluationResponseDTO
)
from app.presentation.api.dependencies import get_initial_evaluation_use_case, get_final_evaluation_use_case
from app.core.exceptions.evaluation_exceptions import (
    EvaluationException,
    EvaluationNotFoundException,
    LLMException,
    InvalidResponseException
)

router = APIRouter(tags=["evaluation"])


@router.post("/initial", response_model=InitialEvaluationResponseDTO)
async def initial_evaluation(
    request: InitialEvaluationRequestDTO,
    use_case: InitialEvaluationUseCase = Depends(get_initial_evaluation_use_case)
) -> InitialEvaluationResponseDTO:
    """
    Perform initial evaluation of user answers.
    
    Evaluates user's answers to determine their current language level
    and provides feedback with suggestions for improvement.
    """
    try:
        return await use_case.execute(request)
    except LLMException as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")
    except InvalidResponseException as e:
        raise HTTPException(status_code=502, detail=f"Invalid LLM response: {str(e)}")
    except EvaluationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/final", response_model=FinalEvaluationResponseDTO)
async def final_evaluation(
    request: FinalEvaluationRequestDTO,
    use_case: FinalEvaluationUseCase = Depends(get_final_evaluation_use_case)
) -> FinalEvaluationResponseDTO:
    """
    Perform final evaluation to determine definitive language level.
    
    Uses the initial evaluation context and new answers to provide
    a final CEFR level determination.
    """
    try:
        return await use_case.execute(request)
    except EvaluationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LLMException as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")
    except EvaluationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")