
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import verify_password
from app.schemas.user import UserLogin


def register_user(db: Session, user_data: UserCreate):
    try:
        existing_user = db.scalar(
            select(User).where(User.email == user_data.email)
        )

        if existing_user is not None:
            raise ValueError("Email already registered")

        new_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")

    except Exception:
        db.rollback()
        raise

def authenticate_user(
    db: Session,
    login_data: UserLogin
):
    user = db.scalar(
        select(User).where(User.email == login_data.email)
    )

    if user is None:
        return None

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        return None

    return user
