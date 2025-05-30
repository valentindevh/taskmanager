from fastapi import APIRouter

from app.api.v1.endpoints import tasks

router = APIRouter(prefix="/api/v1")
router.include_router(tasks.router)