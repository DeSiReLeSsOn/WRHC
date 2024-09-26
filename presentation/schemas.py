from pydantic import (BaseModel, 
                      Field,
                      field_validator)
from datetime import datetime 
from typing import List


class ProductCreateRequest(BaseModel):
    name: str = Field(..., description="Название продукта")
    desc: str = Field(..., description="Описание продукта")
    price: float = Field(..., description="Цена продукта")
    quantity: int = Field(..., description="Количество на складе")


class ProductUpdateRequest(BaseModel):
    name: str = Field(None, description="Название продукта")
    desc: str = Field(None, description="Описание продукта")
    price: float = Field(None, description="Цена продукта")
    quantity: int = Field(None, description="Количество на складе")


class ProductResponse(BaseModel):
    id: str = Field(..., description="ID продукта")
    name: str = Field(..., description="Название продукта")
    desc: str = Field(..., description="Описание продукта")
    price: float = Field(..., description="Цена продукта")
    quantity: int = Field(..., description="Количество на складе") 


class OrderItemRequest(BaseModel):
    product_id: str = Field(..., description="ID продукта")
    quantity: int = Field(..., description="Количество продукта в заказе")


class OrderCreateRequest(BaseModel):
    created_at: datetime = Field(..., description="Дата создания заказа")
    status: str = Field(..., description="Статус заказа")
    items: List[OrderItemRequest] = Field(..., description="Список элементов заказа")

    @field_validator('items', mode='before')
    def validate_items(cls, values):
        if not values:
            raise ValueError("Список элементов заказа должен быть не пустым")
        return values


class OrderItemResponse(BaseModel):
    id: str = Field(..., description="ID элемента заказа")
    product_id: str = Field(..., description="ID продукта")
    quantity: int = Field(..., description="Количество продукта в заказе")


class OrderResponse(BaseModel):
    id: str = Field(..., description="ID заказа")
    created_at: datetime = Field(..., description="Дата создания заказа")
    status: str = Field(..., description="Статус заказа")
    items: List[OrderItemResponse] = Field(..., description="Список элементов заказа")


class OrderUpdateRequest(BaseModel):
    status: str = Field(None, description="Статус заказа")
