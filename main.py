from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.container import Container
from app.core.config.settings import settings
from app.presentation.api.routes.question_routes import router as question_router
from app.presentation.api.routes.evaluation_routes import router as evaluation_router

# --- Inicialización de FastAPI ---
app = FastAPI(
    title=settings.APP_NAME,
    description="A clean architecture API for language evaluation",
    version="2.0.0",
    debug=settings.DEBUG
)

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with detailed messages."""
    errors = [
        {
            "field": ".".join(str(loc) for loc in e["loc"]),
            "message": e["msg"],
            "type": e.get("type", "validation_error")
        }
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"errors": errors})

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME}

@app.get("/debug")
async def debug_endpoint():
    """Debug endpoint to test dependencies."""
    try:
        # Test container
        test_container = container.list_questions_use_case()
        
        # Test direct repository call
        from app.infrastructure.persistence.sqlalchemy.repositories.question_repository_impl import SqlAlchemyQuestionRepository
        repo = SqlAlchemyQuestionRepository()
        questions = repo.find_all()
        
        return {
            "status": "debug_ok",
            "container_works": str(type(test_container)),
            "questions_count": len(questions),
            "questions": [{"id": q.id, "question": q.question} for q in questions[:3]]
        }
    except Exception as e:
        import traceback
        return {
            "status": "debug_error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# --- Inicialización de Container ---
from app.core.container import Container
from app.presentation.api.dependencies import set_container

container = Container()
set_container(container)

# --- Incluir rutas ---
app.include_router(question_router, prefix="/api/v1/questions")
app.include_router(evaluation_router, prefix="/api/v1/evaluation")
