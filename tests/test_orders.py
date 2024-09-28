import pytest
from .conftest import client, order_fixture

@pytest.mark.asyncio
async def test_create_order(client, order_fixture):
    response = client.post("/orders/", json=order_fixture)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == order_fixture["status"]


@pytest.mark.asyncio
async def test_get_order(client, order_fixture):
    create_response = client.post("/orders/", json=order_fixture)
    order_id = create_response.json()["id"]
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == order_id


@pytest.mark.asyncio
async def test_get_all_orders(client, order_fixture):
    client.post("/orders/", json=order_fixture)
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_update_order(client, order_fixture):
    create_response = client.post("/orders/", json=order_fixture)
    order_id = create_response.json()["id"]
    update_data = {"status": "shipped"}
    update_response = client.patch(f"/orders/{order_id}", json=update_data)
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "shipped"

