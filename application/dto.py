from html import entities
from typing import List
from dataclasses import dataclass 
from datetime import datetime 


@dataclass 
class ProductDTO:
    name: str
    desc: str 
    price: float
    quantity: int  


@dataclass 
class OrderDTO:
    created_at: datetime
    status: str
    items: List


@dataclass 
class OrderItemDTO:
    product_id: str
    quantity: int