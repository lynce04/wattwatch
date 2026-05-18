from fastapi import APIRouter
from app.config import PROJECT_NAME, DESCRIPTION
from app.config import VERSION
router = APIRouter(prefix="/api/health", tags=["Health"])

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
        "version" : VERSION,
        "description":DESCRIPTION
    }