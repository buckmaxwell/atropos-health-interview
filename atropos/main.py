from fastapi import FastAPI
from atropos.api import tasks

app = FastAPI(title="Atropos Task API")

app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task API is running"}
