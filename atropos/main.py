from fastapi import FastAPI
from atropos.api import tasks
from atropos.db import init_db

app = FastAPI(title="Atropos Task API")

# Include routers
app.include_router(tasks.router)

# Run database initialization at startup
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Task API is running!"}
