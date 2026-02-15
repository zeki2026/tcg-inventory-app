from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

from app.routers import auth, inventory, dashboard, reports, ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(inventory.router, prefix=f"{settings.API_V1_STR}/cards", tags=["cards"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])
app.include_router(ai.router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])

@app.get("/")
async def root():
    return {"message": "Welcome to TCG Management API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
