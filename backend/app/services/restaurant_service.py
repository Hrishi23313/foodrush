from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Restaurant, User
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def create_restaurant(db: Session, owner: User, data: RestaurantCreate) -> Restaurant:
    duplicate = (
        db.query(Restaurant)
        .filter(
            Restaurant.owner_id == owner.id,
            Restaurant.name == data.name,
            Restaurant.city == data.city,
        )
        .first()
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already registered a restaurant with this name in this city",
        )

    restaurant = Restaurant(owner_id=owner.id, **data.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def list_owner_restaurants(db: Session, owner: User) -> List[Restaurant]:
    return (
        db.query(Restaurant)
        .filter(Restaurant.owner_id == owner.id)
        .order_by(Restaurant.created_at.desc())
        .all()
    )


def get_owned_restaurant(db: Session, owner: User, restaurant_id: int) -> Restaurant:
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id, Restaurant.owner_id == owner.id)
        .first()
    )
    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found"
        )
    return restaurant


def update_restaurant(
    db: Session, owner: User, restaurant_id: int, data: RestaurantUpdate
) -> Restaurant:
    restaurant = get_owned_restaurant(db, owner, restaurant_id)

    changes = data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update"
        )

    for field, value in changes.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant