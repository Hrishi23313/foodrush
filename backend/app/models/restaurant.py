from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import RestaurantStatus


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    cuisine_type = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=True)
    image_url = Column(String(500), nullable=True)
    delivery_fee = Column(Numeric(10, 2), nullable=False, default=0)
    status = Column(
        Enum(RestaurantStatus), nullable=False, default=RestaurantStatus.pending
    )
    is_open = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("User", back_populates="restaurants")
    categories = relationship(
        "Category", back_populates="restaurant", cascade="all, delete-orphan"
    )
    food_items = relationship(
        "FoodItem", back_populates="restaurant", cascade="all, delete-orphan"
    )
    orders = relationship("Order", back_populates="restaurant")