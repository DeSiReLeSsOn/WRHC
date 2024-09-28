import pytest 
from .conftest import client, product_fixture


@pytest.mark.asyncio
async def test_create_product(client, product_fixture):
    response = client.post("/products/", json=product_fixture)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data  
    assert data["name"] == product_fixture["name"]
    assert data["desc"] == product_fixture["desc"]
    assert data["price"] == product_fixture["price"]
    assert data["quantity"] == product_fixture["quantity"]


@pytest.mark.asyncio
async def test_get_product(client, product_fixture):
    create_response = client.post("/products/", json=product_fixture)
    product_id = create_response.json()["id"]  

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == product_id  
    assert data["name"] == product_fixture["name"]


@pytest.mark.asyncio
async def test_get_all_products(client, product_fixture):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  
    assert len(data) > 0  


@pytest.mark.asyncio
async def test_update_product(client, product_fixture):
    create_response = client.post("/products/", json=product_fixture)
    product_id = create_response.json()["id"]  
    update_data = {
        "name": "Updated Product",
        "desc": "Updated Description",
        "price": 75.0,
        "quantity": 30
    }
    update_response = client.put(f"/products/{product_id}", json=update_data)
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Product"  


@pytest.mark.asyncio
async def test_delete_product(client, product_fixture):
    create_response = client.post("/products/", json=product_fixture)
    product_id = create_response.json()["id"]  

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Product deleted"

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404 