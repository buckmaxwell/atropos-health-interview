from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from atropos.api.errors import RecordNotFoundError, InvalidTaskTypeError

from fastapi.requests import Request

from atropos.db import init_db

from atropos.api import tasks
from atropos.api import task_types


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Atropos Task API", lifespan=lifespan)

app.include_router(tasks.router)
app.include_router(task_types.router)


@app.get("/")
def root():
    return {"message": "Task API is running!"}


@app.exception_handler(RecordNotFoundError)
async def record_not_found_handler(request: Request, exc: RecordNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)},
    )


@app.exception_handler(InvalidTaskTypeError)
async def invalid_task_type_handler(request: Request, exc: InvalidTaskTypeError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": ["body", "type"],
                    "msg": f"Unsupported task type: '{exc.task_type}'",
                    "type": "value_error.task_type",
                    "ctx": {"allowed_types": exc.valid_types},
                }
            ]
        },
    )
