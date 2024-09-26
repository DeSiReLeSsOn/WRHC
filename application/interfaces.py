from abc import abstractmethod
from typing import (Protocol, 
                    List, 
                    Optional)
from domain.entities import OrderDM, OrderItemDM, ProductDM


class ProductCreatorInterface(Protocol):
    @abstractmethod
    def create_product(self, product: ProductDM) -> Optional[ProductDM]:
        pass


class ProductReaderInterface(Protocol):
    @abstractmethod
    def get_product(self, product_id: str) -> ProductDM:
        pass


class AllProductReader(Protocol):
    @abstractmethod
    def get_all_products(self) -> List[ProductDM]:
        pass


class ProductUpdaterInterface(Protocol):
    @abstractmethod
    def update_product(self, 
                       product_id: str, 
                       product: ProductDM) -> Optional[ProductDM]:
        pass


class ProductDeleterInterface(Protocol):
    @abstractmethod
    def delete_product(self, product_id: str) -> None:
        pass


class OrderCreatorInterface(Protocol):
    @abstractmethod
    def create_order(self, 
                     order: OrderDM) -> Optional[OrderDM]:
        pass


class AllOrdersReaderInterface(Protocol):
    @abstractmethod
    def get_all_orders(self) -> List[OrderDM]:
        pass


class OrderReaderInterface(Protocol):
    @abstractmethod
    def get_order(self, 
                  order_id: str) -> Optional[OrderDM]:
        pass


class OrderUpdaterInterface(Protocol):
    @abstractmethod
    def update_order(self, 
                     order_id: str, 
                     order: OrderDM) -> Optional[OrderDM]:
        pass


class OrderItemCreatorInterface(Protocol):
    @abstractmethod
    def create_order_item(self, 
                          order_item: OrderItemDM) -> Optional[OrderItemDM]:
        pass



class DBSession(Protocol):
    pass
    # @abstractmethod
    # async def commit(self) -> None:
    #     pass  

    # @abstractmethod    
    # async def flush(self) -> None:
    #     pass


