from dependency_injector import containers, providers
from app.application.evaluation.controllers.evaluation_controller import EvaluationController
from app.application.evaluation.services.evaluation_service import EvaluationService
from app.application.questions.controllers.question_controller import QuestionController
from app.infrastructure.repositories.evaluation_repository import EvaluationRepository
from app.core.langchain_client import LangBuddyLLM
from app.core.openai_client import OpenAIClient
from app.infrastructure.repositories.questions_repositorie_impl import QuestionRepository

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.application.questions.routes.question_routes",
            "app.application.evaluation.routes.evaluation_routes"
        ]
    )

    # Question
    question_repository = providers.Factory(QuestionRepository)
    question_controller = providers.Factory(
        QuestionController,
        repo=question_repository
    )

    # Evaluation
    evaluation_repository = providers.Factory(EvaluationRepository)

    openai_client = providers.Singleton(OpenAIClient)

    langbuddy_llm = providers.Singleton(LangBuddyLLM, client=openai_client)

    evaluation_service = providers.Factory(
    EvaluationService,
    llm=langbuddy_llm,
    question_repo=question_repository
    )


    evaluation_controller = providers.Factory(
        EvaluationController,
        repo=evaluation_repository,
        service=evaluation_service
    )
