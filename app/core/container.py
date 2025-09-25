from dependency_injector import containers, providers

# Core imports
from app.core.config.settings import settings

# Domain services
from app.domain.services.level_calculator import LevelCalculatorService

# Application layer
from app.application.evaluation.use_cases.initial_evaluation_use_case import InitialEvaluationUseCase
from app.application.evaluation.use_cases.final_evaluation_use_case import FinalEvaluationUseCase
from app.application.questions.use_cases.list_questions_use_case import ListQuestionsUseCase

# Infrastructure layer
from app.infrastructure.external_services.langchain_llm_service import LangchainLLMService
from app.infrastructure.persistence.redis.memory_service import RedisMemoryService
from app.infrastructure.persistence.sqlalchemy.repositories.question_repository_impl import SqlAlchemyQuestionRepository
from app.infrastructure.persistence.sqlalchemy.repositories.evaluation_repository_impl import SqlAlchemyEvaluationRepository
from app.infrastructure.persistence.sqlalchemy.repositories.final_evaluation_repository_impl import SqlAlchemyFinalEvaluationRepository


class Container(containers.DeclarativeContainer):
    """Dependency injection container for the application."""
    
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.presentation.api.routes.question_routes",
            "app.presentation.api.routes.evaluation_routes"
        ]
    )

    # Configuration
    config = providers.Configuration()

    # Domain services
    level_calculator_service = providers.Factory(LevelCalculatorService)

    # Infrastructure services
    llm_service = providers.Factory(LangchainLLMService)
    
    memory_service = providers.Factory(RedisMemoryService)

    # Repositories
    question_repository = providers.Factory(SqlAlchemyQuestionRepository)
    evaluation_repository = providers.Factory(SqlAlchemyEvaluationRepository)
    final_evaluation_repository = providers.Factory(SqlAlchemyFinalEvaluationRepository)

    # Use cases
    initial_evaluation_use_case = providers.Factory(
        InitialEvaluationUseCase,
        llm_service=llm_service,
        memory_service=memory_service,
        question_repository=question_repository,
        evaluation_repository=evaluation_repository,
        level_calculator=level_calculator_service
    )

    final_evaluation_use_case = providers.Factory(
        FinalEvaluationUseCase,
        llm_service=llm_service,
        memory_service=memory_service,
        level_calculator=level_calculator_service,
        final_evaluation_repository=final_evaluation_repository
    )

    list_questions_use_case = providers.Factory(
        ListQuestionsUseCase,
        question_repository=question_repository
    )
