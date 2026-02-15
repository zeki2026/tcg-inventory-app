import pytest
import asyncio
import sys
import os
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Add project root to sys.path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db, Base
from app.main import app
from app.config import get_settings
from app.auth_utils import create_access_token

settings = get_settings()

# Use an in-memory SQLite database for testing or a separate test DB
# For async, we need a slight adjustment or use the same PG if user prefers.
# Given the user has a postgres setup in config, let's try to stick to that but maybe use a test database if possible.
# For simplicity in this environment without docker explicit control, let's use sqlite+aiosqlite for tests if possible, 
# OR just mock the session. 
# Better: User wanted "AWS" and real DBs. But locally, sqlite is safer for "run_command" without spinning up postgres.
# However, the code uses `postgresql+asyncpg`. 
# Let's override settings to use sqlite for tests to avoid external dependency issues in this env.

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL, 
    poolclass=NullPool,
)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    # Override get_db dependency
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_token():
    return create_access_token(data={"sub": "test@example.com"})

@pytest.fixture
def test_user_header(test_user_token):
    return {"Authorization": f"Bearer {test_user_token}"}
