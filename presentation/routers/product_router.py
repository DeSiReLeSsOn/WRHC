from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from application.interactors import (
    CreateProductInteractor,
    GetProductInteractor,
    GetAllProductsInteractor,
    UpdateProductInteractor,
    DeleteProductInteractor,
)
from infrastructure.databases.db import get_db_async
from presentation.schemas import (ProductCreateRequest, 
                                  ProductUpdateRequest, 
                                  ProductResponse)

from infrastructure.databases.gateways import (
    ProductGateway
)


product_router = APIRouter()


@product_router.post("/", response_model=ProductResponse)
async def create_product(request: ProductCreateRequest,             
                         db: AsyncSession = Depends(get_db_async)):
    product_gateway = ProductGateway(db)
    interactor = CreateProductInteractor(db, product_gateway=product_gateway)
    try:
        product = await interactor(request)
        if product is None:
            raise HTTPException(status_code=400, detail="Failed to create product")
        return product 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 


@product_router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, 
                      db: AsyncSession = Depends(get_db_async)):
    product_gateway = ProductGateway(db)
    interactor = GetProductInteractor(product_gateway=product_gateway)
    try:
        product = await interactor(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product 
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@product_router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db_async)):
    product_gateway = ProductGateway(db)
    interactor = GetAllProductsInteractor(product_gateway=product_gateway)
    products = await interactor()
    if products is None:
        return []
    return products 



@product_router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, 
                         request: ProductUpdateRequest, 
                         db: AsyncSession = Depends(get_db_async)):
    product_gateway = ProductGateway(db)
    interactor = UpdateProductInteractor(db, product_gateway=product_gateway)
    try:
        product  = await interactor(product_id, request)
        return product 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@product_router.delete("/{product_id}")
async def delete_product(product_id: str, 
                         db: AsyncSession = Depends(get_db_async)):
    product_gateway = ProductGateway(db)
    interactor = DeleteProductInteractor(db, 
                                         product_gateway=product_gateway)
    await interactor(product_id)
    return {"detail": "Product deleted"}
