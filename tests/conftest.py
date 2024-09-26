from fastapi.testclient import TestClient
from main import app
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import pytest

# Set up a test database and session
engine = create_async_engine("sqlite+aiosqlite:///:memory:", poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
async def db_engine():
    async with engine.begin() as conn:
        yield conn

@pytest.fixture(scope="function")
async def db_session(db_engine):
    async with db_engine.begin() as conn:
        async with TestingSessionLocal(bind=conn) as db:
            yield db

client = TestClient(app) 

@pytest.fixture
def test_product():
    product = {
        "name": "b",
        "desc": "b", 
        "price": 12.88, 
        "quantity": 11
    }
    return product