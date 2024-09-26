import pytest
from httpx import AsyncClient
from main import app
from .conftest import test_product


@pytest.mark.asyncio
async def test_create_product(test_product):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json=test_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_product["name"]
    assert data["desc"] == test_product["desc"]
    assert data["price"] == test_product["price"]
    assert data["quantity"] == test_product["quantity"]

@pytest.mark.asyncio
async def test_get_product(test_product):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json=test_product)
        assert response.status_code == 200
        data = response.json()
        product_id = data["id"]
        response = await ac.get(f"/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == test_product["name"]
        assert data["desc"] == test_product["desc"]
        assert data["price"] == test_product["price"]
        assert data["quantity"] == test_product["quantity"]

@pytest.mark.asyncio
async def test_get_all_products(test_product):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json=test_product)
        assert response.status_code == 200
        response = await ac.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_product["name"]
        assert data[0]["desc"] == test_product["desc"]
        assert data[0]["price"] == test_product["price"]
        assert data[0]["quantity"] == test_product["quantity"]

@pytest.mark.asyncio
async def test_update_product(test_product):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json=test_product)
        assert response.status_code == 200
        data = response.json()
        product_id = data["id"]
        updated_product = {
            "name": "updated name",
            "desc": "updated desc",
            "price": 99.99,
            "quantity": 100
        }
        response = await ac.put(f"/products/{product_id}", json=updated_product)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == updated_product["name"]
        assert data["desc"] == updated_product["desc"]
        assert data["price"] == updated_product["price"]
        assert data["quantity"] == updated_product["quantity"]

@pytest.mark.asyncio
async def test_delete_product(test_product):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json=test_product)
        assert response.status_code == 200
        data = response.json()
        product_id = data["id"]
        response = await ac.delete(f"/products/{product_id}")
        assert response.status_code == 200
        response = await ac.get(f"/products/{product_id}")
        assert response.status_code == 404