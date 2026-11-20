from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, func,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    restaurant_name = Column(String(150), nullable=False)
    delivery_name = Column(String(100), nullable=False)
    delivery_phone = Column(String(20), nullable=False)
    delivery_address = Column(String(500), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.placed)
    status_reason = Column(String(255), nullable=True)
    notes = Column(String(500), nullable=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    delivery_fee = Column(Numeric(10, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    placed_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    customer = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    payment = relationship(
        "Payment", back_populates="order", uselist=False, cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=True)
    item_name = Column(String(150), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    line_total = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    food_item = relationship("FoodItem")