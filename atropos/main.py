from fastapi import FastAPI

app = FastAPI(title="Atropos Task API")


@app.get("/")
def root():
    return {"message": "Task API is running!"}
