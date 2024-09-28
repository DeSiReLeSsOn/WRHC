import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from main import create_app  
from infrastructure.databases.models import Product
from datetime import datetime 


Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  
    poolclass=StaticPool
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


@pytest.fixture(scope="module")
async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  

    yield 

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  




@pytest.fixture
def client(init_test_db):
    app = create_app()
    with TestClient(app) as c:
        yield c 




@pytest.fixture
def product_fixture():
    product = {
        "id": "1",
        "name": "Test product", 
        "desc": "test desc",
        "price": 12.99, 
        "quantity": 99
    }

    return product 



@pytest.fixture
def order_fixture(client):
    product_response = client.post("/products/", json={
        "name": "Test Product",
        "desc": "Test Description",
        "price": 100.0,
        "quantity": 50
    })
    product_id = product_response.json()["id"]
    
    return {
        "created_at": datetime.now().isoformat(),  
        "status": "pending",
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }