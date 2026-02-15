import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_card(client: AsyncClient):
    # Register and login to get token
    await client.post(
        "/api/v1/auth/register",
        json={"email": "cardowner@example.com", "password": "pass", "role": "free"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "cardowner@example.com", "password": "pass"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create card
    response = await client.post(
        "/api/v1/cards/",
        json={
            "name": "Black Lotus",
            "purchase_price": 10000.0,
            "condition": "Mint" # Note: schema might differ, checking later
        },
        headers=headers
    )
    # Note: I need to verify schemas.py for exact fields. 
    # Based on models.py seen earlier: name, purchase_price, current_market_price, grade, status
    # Let's adjust payload to match standard expectation or models
    
    # Correction based on previous `models.py` view:
    # name, purchase_price, current_market_price, grade, status
    
    response = await client.post(
        "/api/v1/cards/",
        json={
            "name": "Black Lotus",
            "purchase_price": 10000.0,
            "grade": "PSA 10"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Black Lotus"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_read_cards(client: AsyncClient):
    # Register/Login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "viewer@example.com", "password": "pass", "role": "free"}
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "viewer@example.com", "password": "pass"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a card first
    await client.post(
        "/api/v1/cards/",
        json={"name": "Charizard", "purchase_price": 500.0, "grade": "PSA 9"},
        headers=headers
    )

    # List cards
    response = await client.get("/api/v1/cards/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Charizard"
