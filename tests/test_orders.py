import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from infrastructure.databases.db import init_db
from presentation.routers.order_router import order_router


app = FastAPI()
app.include_router(order_router)


client = TestClient(app)


@pytest.fixture
async def db():
    async with init_db() as db:
        yield db


@pytest.mark.asyncio
async def test_create_order(db):
    request = {
        "created_at": "2022-01-01T00:00:00",
        "status": "в процессе",
        "items": [
            {
                "product_id": "1",
                "quantity": 1
            }
        ]
    }
    response = client.post("/orders/", json=request)
    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["created_at"] == request["created_at"]
    assert response.json()["status"] == request["status"]
    assert response.json()["items"] == request["items"]


@pytest.mark.asyncio
async def test_get_order(db):
    request = {
        "created_at": "2022-01-01T00:00:00",
        "status": "в процессе",
        "items": [
            {
                "product_id": "1",
                "quantity": 1
            }
        ]
    }
    response = await client.post("/orders/", json=request)
    order_id = response.json()["id"]
    response = await client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["created_at"] == request["created_at"]
    assert response.json()["status"] == request["status"]
    assert response.json()["items"] == request["items"]


@pytest.mark.asyncio
async def test_get_all_orders(db):
    request1 = {
        "created_at": "2022-01-01T00:00:00",
        "status": "в процессе",
        "items": [
            {
                "product_id": "1",
                "quantity": 1
            }
        ]
    }
    request2 = {
        "created_at": "2022-01-02T00:00:00",
        "status": "отправлен",
        "items": [
            {
                "product_id": "2",
                "quantity": 2
            }
        ]
    }
    await client.post("/orders/", json=request1)
    await client.post("/orders/", json=request2)
    response = await client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_order(db):
    request = {
        "created_at": "2022-01-01T00:00:00",
        "status": "в процессе",
        "items": [
            {
                "product_id": "1",
                "quantity": 1
            }
        ]
    }
    response = await client.post("/orders/", json=request)
    order_id = response.json()["id"]
    update_request = {
        "status": "отправлен"
    }
    response = await client.patch(f"/orders/{order_id}", json=update_request)
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["status"] == update_request["status"]