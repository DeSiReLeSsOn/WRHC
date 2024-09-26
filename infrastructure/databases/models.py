from sqlalchemy import (Column, 
                        String, 
                        Integer, 
                        Float, 
                        ForeignKey, 
                        DateTime)
from sqlalchemy.orm import relationship, declarative_base



Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    desc = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    items = relationship("OrderItem", backref="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False) 


