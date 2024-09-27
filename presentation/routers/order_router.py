from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from application.interactors import (
    CreateOrderInteractor,
    GetOrderInteractor,
    GetAllOrdersInteractor,
    UpdateOrderInteractor,
)
from infrastructure.databases.db import get_db_async
from infrastructure.databases.gateways import (
    OrderGateway,
    OrderItemGateway,
    ProductGateway,
)
from presentation.schemas import (
    OrderCreateRequest,
    OrderUpdateRequest,
    OrderResponse,
)

order_router = APIRouter()


@order_router.post("/", response_model=OrderResponse)
async def create_order(request: OrderCreateRequest, 
                       db: AsyncSession = Depends(get_db_async)):
    order_gateway = OrderGateway(db, OrderItemGateway(db))
    product_gateway = ProductGateway(db)
    interactor = CreateOrderInteractor(db, 
                                       order_gateway=order_gateway, 
                                       order_item_gateway=order_gateway._order_item_repository, 
                                       product_reader=product_gateway, 
                                       product_updater=product_gateway)
    try:
        order = await interactor(request, request.items)
        if order is None:
            raise HTTPException(status_code=400)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@order_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, 
                    db: AsyncSession = Depends(get_db_async)):
    order_gateway = OrderGateway(db, OrderItemGateway(db))
    interactor = GetOrderInteractor(order_gateway=order_gateway)
    try:
        order = await interactor(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@order_router.get("/", response_model=List[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db_async)):
    order_gateway = OrderGateway(db, OrderItemGateway(db))
    interactor = GetAllOrdersInteractor(orders_gateway=order_gateway)
    try:
        orders = await interactor()
        if orders is None:
            raise HTTPException(status_code=404, detail="Orders not found")
        return orders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@order_router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, 
                       request: OrderUpdateRequest, 
                       db: AsyncSession = Depends(get_db_async)):
    if not request.status:
        raise HTTPException(status_code=400, detail="Status is required")
    order_gateway = OrderGateway(db, OrderItemGateway(db))
    interactor = UpdateOrderInteractor(db, 
                                       order_reader=order_gateway, 
                                       order_gateway=order_gateway)
    try:
        order = await interactor(order_id, request.status)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))