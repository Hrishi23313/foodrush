from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import require_owner
from app.models import User
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services import restaurant_service

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.post("", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def register_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    owner: User = Depends(require_owner),
):
    return restaurant_service.create_restaurant(db, owner, data)


@router.get("/my", response_model=List[RestaurantResponse])
def my_restaurants(
    db: Session = Depends(get_db), owner: User = Depends(require_owner)
):
    return restaurant_service.list_owner_restaurants(db, owner)


@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
def update_my_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: Session = Depends(get_db),
    owner: User = Depends(require_owner),
):
    return restaurant_service.update_restaurant(db, owner, restaurant_id, data)