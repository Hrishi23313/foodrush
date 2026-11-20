from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    method = Column(Enum(PaymentMethod), nullable=False, default=PaymentMethod.cod)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    amount = Column(Numeric(10, 2), nullable=False)
    provider_payment_id = Column(String(100), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payment")