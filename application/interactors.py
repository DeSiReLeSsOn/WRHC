from typing import List, Optional 
import uuid
from application.dto import (OrderDTO, 
                             OrderItemDTO, 
                             ProductDTO)
from application.interfaces import (
                                    AllOrdersReaderInterface, 
                                    AllProductReader, 
                                    OrderCreatorInterface, 
                                    OrderItemCreatorInterface, 
                                    OrderReaderInterface, 
                                    OrderUpdaterInterface,  
                                    ProductCreatorInterface, 
                                    ProductDeleterInterface, 
                                    ProductReaderInterface, 
                                    ProductUpdaterInterface,
                                    DBSession)
from domain.entities import (OrderDM, 
                             OrderItemDM, 
                             ProductDM) 


class CreateProductInteractor:
    def __init__(self, 
                 db_session: DBSession,
                 product_gateway: ProductCreatorInterface):
        self._db_session = db_session
        self._product_gateway = product_gateway 

    async def __call__(self, 
                       dto: ProductDTO) -> Optional[ProductDM]:
        product_id = str(uuid.uuid4())
        product = ProductDM(
            id=product_id,
            name=dto.name, 
            desc=dto.desc, 
            price=dto.price, 
            quantity=dto.quantity
        )

        product = await self._product_gateway.create_product(product)
        return product
    

class GetProductInteractor:
    def __init__(self, 
                 product_gateway: ProductReaderInterface) :
        self._product_gateway = product_gateway

    async def __call__(self, product_id: str) -> Optional[ProductDM]:
        if not product_id:
            return None
        product = await self._product_gateway.get_product(product_id)
        if product is None: 
            raise ValueError(f"Product with supplied id: {product_id} not exist")
        return product
    

class GetAllProductsInteractor:
    def __init__(self, product_gateway: AllProductReader):
        self._products_gateway = product_gateway 

    async def __call__(self) -> List[ProductDM]:
        products = await self._products_gateway.get_all_products()
        if products is None:
            return []
        return products
    

class UpdateProductInteractor:
    def __init__(self, 
                 db_session: DBSession, 
                 product_gateway: ProductUpdaterInterface,
                 ):
        self._db_session = db_session
        self._product_gateway = product_gateway 

    async def __call__(self, product_id: str, 
                       dto: ProductDTO) -> Optional[ProductDM]:
        if not product_id:
            return None
        product = ProductDM(
            id=product_id, 
            name=dto.name, 
            desc=dto.desc, 
            price=dto.price,
            quantity=dto.quantity
        ) 
        product = await self._product_gateway.update_product(product_id, product)
        if product is None:
            return None
        await self._db_session.commit() 
        return product  

    
class DeleteProductInteractor:
    def __init__(self,
                 db_session: DBSession, 
                 product_gateway: ProductDeleterInterface,):
        self._db_session = db_session 
        self._product_gateway = product_gateway

    async def __call__(self, product_id: str) -> None:
        if product_id is None:
            return None
        await self._product_gateway.delete_product(product_id)
        await self._db_session.commit()
        return None


class CreateOrderInteractor:
    def __init__(self,
                 db_session: DBSession,
                 order_gateway: OrderCreatorInterface,
                 order_item_gateway: OrderItemCreatorInterface,
                 product_reader: ProductReaderInterface,
                 product_updater: ProductUpdaterInterface,
                 ):
        self._db_session = db_session
        self._order_gateway = order_gateway
        self._order_item_gateway = order_item_gateway
        self._product_reader = product_reader
        self._product_updater = product_updater

    async def __call__(self,
                       dto: OrderDTO,
                       items_dto: List[OrderItemDTO]) -> Optional[OrderDM]:
        order_id = str(uuid.uuid4())
        order = OrderDM(
            id=order_id,
            created_at=dto.created_at,
            status=dto.status,
            items=[]
        )
        order = await self._order_gateway.create_order(order)
        if order is None:
            return None
        for items in items_dto:
            product = await self._product_reader.get_product(items.product_id)
            if product is None:
                raise ValueError(f"Product with supplied id: {items.product_id} not exist")
            if product.quantity < items.quantity:
                raise ValueError("Not enough product at warehouse")
            order_item = OrderItemDM(
                id=str(uuid.uuid4()),
                order_id=order_id,
                product_id=items.product_id,
                quantity=items.quantity
            )
            order.items.append(order_item)
            product.quantity -= items.quantity
            await self._product_updater.update_product(items.product_id, product)
            await self._order_item_gateway.create_order_item(order_item)

        await self._db_session.commit()
        return order
        
            
class GetOrderInteractor:
    def __init__(self, order_gateway: OrderReaderInterface):
        self._order_gateway = order_gateway 

    async def __call__(self, order_id: str) -> Optional[OrderDM]:
        if not order_id:
            return None
        order = await self._order_gateway.get_order(order_id)
        if order is None:
            raise ValueError(f"Order with supplied id: {order_id} not exist")
        return order


class GetAllOrdersInteractor:
    def __init__(self, orders_gateway: AllOrdersReaderInterface):
        self._orders_gateway = orders_gateway 

    async def __call__(self) -> List[OrderDM]:
        orders = await self._orders_gateway.get_all_orders()
        if orders is None:
            return []
        return orders 
    

class UpdateOrderInteractor:
    def __init__(self, db_session: DBSession, 
                 order_reader: OrderReaderInterface,
                 order_gateway: OrderUpdaterInterface):
        self._db_session = db_session
        self._order_gateway = order_gateway
        self._order_reader = order_reader

    async def __call__(self, 
                       order_id: str, 
                       status: str) -> Optional[OrderDM]:
        if not order_id:
            return None
        existing_order = await self._order_reader.get_order(order_id)
        if existing_order is None:
            return None
        existing_order.status = status
        order = await self._order_gateway.update_order(order_id, existing_order)
        if order is None:
            return None
        await self._db_session.commit()
        return order
    

class CreateOrderItemInteractor:
    def __init__(self,
                 order_item_gateway: OrderItemCreatorInterface):
        self._order_item_gateway = order_item_gateway

    async def __call__(self, order_id: str, dto: OrderItemDTO) -> OrderItemDM:
        order_item_id = str(uuid.uuid4())
        order_item = OrderItemDM(
            id=order_item_id,
            order_id=order_id,
            product_id=dto.product_id,
            quantity=dto.quantity
        )
        order_item = await self._order_item_gateway.create_order_item(order_item)
        if order_item is None:
            return None
        return order_item





        


