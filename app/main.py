from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.health  import router_info as app_info

app = FastAPI(
    title="WattWatch",
    description="Energy market data API for Germany",
    version="1.0.0"
)
app.include_router(health_router)
app.include_router(app_info)

