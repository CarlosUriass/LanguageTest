from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.container import Container
from app.application.questions.routes.question_routes import router as question_router
from app.application.evaluation.routes.evaluation_routes import router as evaluation_router

# --- Inicialización de FastAPI ---
app = FastAPI(title="Language Test API")

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(loc) for loc in e["loc"]),
            "message": e["msg"],
            "type": e.get("type", "validation_error")
        }
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"errors": errors})

# --- Inicialización de Container ---
container = Container()
container.wire(
    modules=[
        "app.application.questions.routes.question_routes",
        "app.application.evaluation.routes.evaluation_routes"
    ]
)
# --- Incluir rutas ---
app.include_router(question_router, prefix="/questions")
app.include_router(evaluation_router, prefix="/evaluation")
