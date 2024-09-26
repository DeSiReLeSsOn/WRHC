from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum


@dataclass
class ProductDM:
    id: str
    name: str
    desc: str 
    price: float
    quantity: int 


@dataclass 
class OrderDM:
    id: str
    created_at: datetime
    status: str 
    items: List


@dataclass 
class OrderItemDM:
    id: str
    order_id: str
    product_id: str
    quantity: int






