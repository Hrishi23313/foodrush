from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="categories")
    food_items = relationship("FoodItem", back_populates="category")