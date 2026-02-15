import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "role": "free"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # First register
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "loginuser@example.com",
            "password": "password123",
            "role": "free"
        }
    )
    
    # Then login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "loginuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
