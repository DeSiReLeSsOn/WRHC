from fastapi import FastAPI  
import uvicorn
from presentation.routers.order_router import order_router
from presentation.routers.product_router import product_router
from infrastructure.databases.db import init_db, close_db


app = FastAPI() 


app.include_router(product_router, prefix="/products")
app.include_router(order_router, prefix="/orders") 


@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)