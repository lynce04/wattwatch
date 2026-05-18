from fastapi import FastAPI

app = FastAPI(
    title="WattWatch",
    description="Energy market data API for Germany",
    version="1.0.0"
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "project": "WattWatch"
    }