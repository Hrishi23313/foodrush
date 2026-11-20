from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.customer)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    restaurants = relationship("Restaurant", back_populates="owner")
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    cart = relationship(
        "Cart", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    orders = relationship("Order", back_populates="customer")