from fastapi import FastAPI
from atropos.api import tasks
from contextlib import asynccontextmanager
from atropos.db import init_db


# Run database initialization at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # ← put your startup logic here
    yield
    # Optional: shutdown/cleanup logic here


app = FastAPI(title="Atropos Task API", lifespan=lifespan)

# Include routers
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task API is running!"}
