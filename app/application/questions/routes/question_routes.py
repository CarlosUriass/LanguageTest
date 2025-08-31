from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.application.questions.controllers.question_controller import QuestionController
from app.core.container import Container

router = APIRouter()

@router.get("/")
@inject
def list_questions(controller: QuestionController = Depends(Provide[Container.question_controller])):
    return controller.list_questions()
