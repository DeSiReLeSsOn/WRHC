import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from infrastructure.databases.db import init_db, close_db, get_db_async
from presentation.schemas import ProductCreateRequest, ProductUpdateRequest
from main import app  # Импортируйте ваше приложение FastAPI

DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # Используйте in-memory SQLite для тестов

@pytest.fixture
async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    # Инициализация базы данных
    async with engine.begin() as conn:
        await init_db(conn)

    yield async_session

    await engine.dispose()

@pytest.fixture
async def client(test_db):
    async def override_get_db():
        async with test_db() as session:
            yield session
            
    app.dependency_overrides[get_db_async] = override_get_db
    yield TestClient(app)

@pytest.mark.asyncio
async def test_create_product(client):
    product_data = ProductCreateRequest(name="Test Product", desc="Test Description", price=10.99, quantity=100)
    response = client.post("/products/", json=product_data.model_dump())  # Используем model_dump()
    
    assert response.status_code == 200
    created_product = response.json()
    assert created_product["name"] == product_data.name
    assert created_product["desc"] == product_data.desc
    assert created_product["price"] == product_data.price
    assert created_product["quantity"] == product_data.quantity

@pytest.mark.asyncio
async def test_get_product(client):
    # Создайте продукт для теста
    product_data = ProductCreateRequest(name="Test Product", desc="Test Description", price=10.99, quantity=100)
    response = client.post("/products/", json=product_data.model_dump())  # Используем model_dump()
    created_product = response.json()

    product_id = created_product["id"]
    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id
    assert product["name"] == product_data.name

@pytest.mark.asyncio
async def test_get_all_products(client):
    product_data1 = ProductCreateRequest(name="Product 1", desc="Description 1", price=10.99, quantity=100)
    product_data2 = ProductCreateRequest(name="Product 2", desc="Description 2", price=20.99, quantity=200)
    
    client.post("/products/", json=product_data1.model_dump())  # Используем model_dump()
    client.post("/products/", json=product_data2.model_dump())  # Используем model_dump()
    
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 2  # Должно вернуть как минимум 2 продукта

@pytest.mark.asyncio
async def test_update_product(client):
    # Создайте продукт для теста
    product_data = ProductCreateRequest(name="Test Product", desc="Test Description", price=10.99, quantity=100)
    response = client.post("/products/", json=product_data.model_dump())  # Используем model_dump()
    created_product = response.json()

    product_id = created_product["id"]
    update_data = ProductUpdateRequest(name="Updated Product", desc="Updated Description", price=15.99, quantity=150)
    response = client.put(f"/products/{product_id}", json=update_data.model_dump())  # Используем model_dump()

    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["name"] == update_data.name

@pytest.mark.asyncio
async def test_delete_product(client):
    # Создайте продукт для теста
    product_data = ProductCreateRequest(name="Test Product", desc="Test Description", price=10.99, quantity=100)
    response = client.post("/products/", json=product_data.model_dump())  # Используем model_dump()
    created_product = response.json()

    product_id = created_product["id"]
    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted"}

    # Проверьте, что продукт был удален
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404  # Продукт не должен существовать