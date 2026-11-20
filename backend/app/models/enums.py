import enum


class UserRole(str, enum.Enum):
    customer = "customer"
    owner = "owner"
    admin = "admin"


class RestaurantStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    suspended = "suspended"


class OrderStatus(str, enum.Enum):
    placed = "placed"
    accepted = "accepted"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"
    rejected = "rejected"
    cancelled = "cancelled"


class PaymentMethod(str, enum.Enum):
    cod = "cod"
    razorpay = "razorpay"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"