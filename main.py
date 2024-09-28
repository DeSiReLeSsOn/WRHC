from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from presentation.routers.order_router import order_router
from presentation.routers.product_router import product_router
from infrastructure.databases.db import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


def create_app():
    app = FastAPI(lifespan=lifespan)  
    app.include_router(product_router, prefix="/products")
    app.include_router(order_router, prefix="/orders")
    return app


if __name__ == '__main__':
    uvicorn.run("main:create_app", host="0.0.0.0", port=8080, reload=True, factory=True)