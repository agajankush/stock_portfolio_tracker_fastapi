# tests/test_api.py

import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    """
    Tests the root endpoint of the application.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Stock Portfolio API!"}