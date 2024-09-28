from typing import List, Optional
from datetime import datetime
from application.interfaces import (
    ProductReaderInterface,
    AllProductReader,
    ProductCreatorInterface,
    ProductUpdaterInterface,
    ProductDeleterInterface,
    OrderItemCreatorInterface,
    OrderCreatorInterface,
    OrderReaderInterface,
    AllOrdersReaderInterface,
    OrderUpdaterInterface,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update
from sqlalchemy.orm import joinedload


from .models import (Product, 
                    OrderItem, 
                    Order)
from domain.entities import (ProductDM, 
                             OrderDM, 
                             OrderItemDM)


class ProductGateway(
    ProductCreatorInterface,
    ProductReaderInterface,
    AllProductReader,
    ProductUpdaterInterface,
    ProductDeleterInterface,
):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, product: ProductDM) -> ProductDM:
        db_product = Product(
            id=product.id,
            name=product.name,
            desc=product.desc,
            price=product.price,
            quantity=product.quantity,
        )
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return ProductDM(
            id=db_product.id,
            name=db_product.name,
            desc=db_product.desc,
            price=db_product.price,
            quantity=db_product.quantity,
        )

    async def get_product(self, product_id: str) -> ProductDM:
        db_product = await self.db.get(Product, product_id)
        if db_product is None:
            raise ValueError(f"Product with ID {product_id} not found")
        return ProductDM(
            id=db_product.id,
            name=db_product.name,
            desc=db_product.desc,
            price=db_product.price,
            quantity=db_product.quantity,
        )

    async def get_all_products(self) -> List[ProductDM]:
        query = select(Product)
        result = await self.db.execute(query)
        db_products = result.scalars().all()
        if not db_products:
            return []
        return [
            ProductDM(id=db_product.id, 
                      name=db_product.name, 
                      desc=db_product.desc,
                        price=db_product.price, 
                        quantity=db_product.quantity)
            for db_product in db_products
        ]
    
    async def update_product(self, product_id: str, product: ProductDM) -> Optional[ProductDM]:
        query = update(Product).where(Product.id == product_id).values(
            name=product.name,
            desc=product.desc,
            price=product.price,
            quantity=product.quantity,
        )
        result = await self.db.execute(query)
        if result.rowcount == 0:
            raise ValueError(f"Product with ID {product_id} not found")
        await self.db.commit()
        return product

    async def delete_product(self, product_id: str) -> None:
        db_product = await self.db.get(Product, product_id)
        if db_product is None:
            raise ValueError(f"Product with ID {product_id} not found")
        await self.db.delete(db_product)
        await self.db.commit() 


class OrderItemGateway(
    OrderItemCreatorInterface,
):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order_item(self, order_item: OrderItemDM) -> OrderItemDM:
        db_order_item = OrderItem(
            id=order_item.id,
            order_id=order_item.order_id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
        )
        self.db.add(db_order_item)
        await self.db.commit()
        await self.db.refresh(db_order_item)
        return order_item


class OrderGateway(
    OrderCreatorInterface,
    OrderReaderInterface,
    AllOrdersReaderInterface,
    OrderUpdaterInterface,
):
    def __init__(self, 
                 db: AsyncSession, 
                 order_item_gateway: OrderItemGateway):
        self.db = db
        self._order_item_gateway = order_item_gateway

    async def create_order(self, order: OrderDM) -> OrderDM:
        db_order = Order(
            id=order.id,
            created_at=datetime.now(),
            status=order.status,
        )
        for item in order.items:
            db_item = await self._order_item_gateway.create_order_item(item)
            db_order.items.append(db_item)
        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)
        return order

    async def get_all_orders(self) -> List[OrderDM]:
        query = select(Order).options(joinedload(Order.items))
        result = await self.db.execute(query)
        db_orders = result.unique().scalars().all() 
        return [
            OrderDM(
                id=db_order.id,
                created_at=db_order.created_at,
                status=db_order.status,
                items=[
                    OrderItemDM(
                        id=item.id,
                        order_id=db_order.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                    )
                    for item in db_order.items
                ],
            )
            for db_order in db_orders
        ]
    
    async def get_order(self, order_id: str) -> OrderDM:
        query = select(Order).options(joinedload(Order.items)).filter(Order.id == order_id)
        result = await self.db.execute(query) 
        db_order = result.unique().scalar_one_or_none() 
        if db_order is None:
            raise ValueError(f"Order with ID {order_id} not found")
        return OrderDM(
            id=db_order.id,
            created_at=db_order.created_at,
            status=db_order.status,
            items=[
                OrderItemDM(
                    id=item.id,
                    order_id=db_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
                for item in db_order.items
            ],
        )
    
    async def update_order(self, 
                           order_id: str, 
                           order: OrderDM) -> Optional[OrderDM]:
        query = update(Order).where(Order.id == order_id).values(status=order.status)
        result = await self.db.execute(query)
        if result.rowcount == 0:
            raise ValueError(f"Order with ID {order_id} not found")
        await self.db.commit()
        return order