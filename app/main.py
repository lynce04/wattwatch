from fastapi import FastAPI
from app.api.health import router as health_router
from database.base import Base
from database.session import engine
from database import *


app = FastAPI(
    title="WattWatch",
    description="Energy market data API for Germany",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(health_router)

