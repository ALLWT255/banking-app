
from fastapi import FastAPI

from app.api.routes import health, accounts, transactions, users, ops

app = FastAPI(
    title="Banking API",
    description="Cloud-native banking application",
    version="1.0.0"
)

app.include_router(health.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(ops.router, prefix="/api")
