from fastapi import APIRouter, Depends

from app.middleware.auth import require_admin, require_customer, require_owner
from app.models import User

router = APIRouter(prefix="/role-test", tags=["Role test (temporary)"])


@router.get("/customer")
def customer_only(user: User = Depends(require_customer)):
    return {"message": f"Hello customer {user.full_name}"}


@router.get("/owner")
def owner_only(user: User = Depends(require_owner)):
    return {"message": f"Hello owner {user.full_name}"}


@router.get("/admin")
def admin_only(user: User = Depends(require_admin)):
    return {"message": f"Hello admin {user.full_name}"}