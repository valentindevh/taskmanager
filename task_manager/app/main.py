from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings

app = FastAPI(title="Task Management API")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Task Management API"}