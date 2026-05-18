from fastapi import APIRouter
from app.config import PROJECT_NAME
from app.config import VERSION
router = APIRouter(prefix="/api/health", tags=["Health"])

router_info = APIRouter(prefix="/api/health/info")
@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "project": PROJECT_NAME
    }
@router.get("/info")
def app_info():
    return {
        "project": PROJECT_NAME,
        "version" : "1.0.0",
        "description": " This is a solid FastAPI backend for energy data from SMARD.de "
    }