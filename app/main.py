from fastapi import FastAPI
from app.config import get_settings
from app.database import get_db
from sqlalchemy.future import select
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, Request
settings = get_settings()

from app.routers import auth, inventory, dashboard, reports, ai

from fastapi.middleware.cors import CORSMiddleware
from app.core.token_middleware import token_middleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]


# @app.middleware("http")
# async def middleware_token(request: Request, call_next) -> Response:
#     return await token_middleware(request, call_next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/healthdb")
async def health_check(db: AsyncSession = Depends(get_db)):
    result  = await db.scalar(select(1))  
    if result is None:
        raise HTTPException(status_code=500, detail="Database connection failed") 
    return {"status": "ok","response":result}