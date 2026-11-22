from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import RestaurantStatus

PHONE_PATTERN = r"^\+?[0-9]{10,15}$"
PINCODE_PATTERN = r"^[0-9]{6}$"


class RestaurantCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=2000)
    cuisine_type: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, pattern=PHONE_PATTERN)
    address: str = Field(min_length=5, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    pincode: Optional[str] = Field(default=None, pattern=PINCODE_PATTERN)
    image_url: Optional[str] = Field(default=None, max_length=500)
    delivery_fee: Decimal = Field(
        default=Decimal("0.00"), ge=0, max_digits=8, decimal_places=2
    )


class RestaurantUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = Field(default=None, max_length=2000)
    cuisine_type: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, pattern=PHONE_PATTERN)
    address: Optional[str] = Field(default=None, min_length=5, max_length=255)
    city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    pincode: Optional[str] = Field(default=None, pattern=PINCODE_PATTERN)
    image_url: Optional[str] = Field(default=None, max_length=500)
    delivery_fee: Optional[Decimal] = Field(
        default=None, ge=0, max_digits=8, decimal_places=2
    )
    is_open: Optional[bool] = None

    @field_validator("name", "address", "city", "delivery_fee", "is_open")
    @classmethod
    def required_columns_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value


class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    phone: Optional[str] = None
    address: str
    city: str
    pincode: Optional[str] = None
    image_url: Optional[str] = None
    delivery_fee: Decimal
    status: RestaurantStatus
    is_open: bool
    created_at: datetime
    updated_at: datetime