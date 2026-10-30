from fastapi import FastAPI

app = FastAPI(
    title="Banking API",
    description="Cloud-native banking application",
    version="1.0.0"
)
from app.api.routes import health

app.include_router(health.router, prefix="/api")