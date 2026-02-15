import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_dashboard_roi_anonymous(client: AsyncClient):
    # Should fail without auth
    response = await client.get("/api/v1/dashboard/roi")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_dashboard_roi_authenticated(client: AsyncClient):
    # Setup user
    await client.post(
        "/api/v1/auth/register",
        json={"email": "roi@example.com", "password": "pass", "role": "pro"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "roi@example.com", "password": "pass"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get("/api/v1/dashboard/roi", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "roi_percentage" in data

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
