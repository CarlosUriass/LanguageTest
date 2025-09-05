from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.application.evaluation.controllers.evaluation_controller import EvaluationController
from app.application.evaluation.dtos.final_evaluation_dto import FinalEvaluationListDTO
from app.application.evaluation.dtos.initial_evaluation_dto import InitialEvaluationListDTO
from app.core.container import Container

router = APIRouter()

@router.post("/initial")
@inject
def evaluate_answers(
    evaluation_dto: InitialEvaluationListDTO,
    controller: EvaluationController = Depends(Provide[Container.evaluation_controller])
):
    result = controller.evaluate(evaluation_dto)

    return result

@router.post("/final")
@inject
def final_evaluation(
    evaluation_dto: FinalEvaluationListDTO,
    controller: EvaluationController = Depends(Provide[Container.evaluation_controller])
):
    result = controller.evaluate_final(evaluation_dto)

    print(result)
    
    return result