from getpass import getpass

from app.database import SessionLocal
from app.models import User
from app.models.enums import UserRole
from app.utils.security import hash_password


def main():
    full_name = input("Admin full name: ").strip()
    email = input("Admin email: ").strip().lower()
    password = getpass("Admin password (hidden): ")

    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return

    with SessionLocal() as db:
        if db.query(User).filter(User.email == email).first():
            print("A user with this email already exists.")
            return

        admin = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role=UserRole.admin,
        )
        db.add(admin)
        db.commit()
        print(f"Admin created: {email}")


if __name__ == "__main__":
    main()