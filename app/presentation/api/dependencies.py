from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.application.evaluation.use_cases.initial_evaluation_use_case import InitialEvaluationUseCase
    from app.application.evaluation.use_cases.final_evaluation_use_case import FinalEvaluationUseCase
    from app.application.questions.use_cases.list_questions_use_case import ListQuestionsUseCase

# Contenedor global que se inicializará desde main.py
_container = None

def set_container(container):
    """Set the global container instance."""
    global _container
    _container = container

def get_initial_evaluation_use_case() -> "InitialEvaluationUseCase":
    """Dependency injection for initial evaluation use case."""
    if _container is None:
        raise RuntimeError("Container not initialized")
    return _container.initial_evaluation_use_case()


def get_final_evaluation_use_case() -> "FinalEvaluationUseCase":
    """Dependency injection for final evaluation use case."""
    if _container is None:
        raise RuntimeError("Container not initialized")
    return _container.final_evaluation_use_case()


def get_list_questions_use_case() -> "ListQuestionsUseCase":
    """Dependency injection for list questions use case."""
    if _container is None:
        raise RuntimeError("Container not initialized")
    return _container.list_questions_use_case()