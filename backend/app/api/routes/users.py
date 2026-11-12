
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate
from app.services.user_service import register_user
from app.schemas.user import UserLogin
from app.services.user_service import authenticate_user
from app.core.security import create_access_token

router = APIRouter()


@router.post("/users/register", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, user_data)

        return {
            "id": user.id,
            "email": user.email
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.post("/users/login")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, login_data)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
