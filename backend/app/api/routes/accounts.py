from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal

from app.db.session import get_db
from app.models.account import Account
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.account import AccountCreate
from app.core.security import get_current_user_id
router = APIRouter()


@router.get("/accounts")
def get_accounts(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    accounts = (
        db.query(Account)
        .filter(Account.user_id == current_user_id)
        .all()
    )

    return [
        {
            "id": account.id,
            "user_id": account.user_id,
            "account_type": account.account_type,
            "balance": str(account.balance)
        }
        for account in accounts
    ]


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    user = db.get(User, current_user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user not found"
        )

    new_account = Account(
        user_id=current_user_id,
        account_type=account_data.account_type,
        balance=Decimal("0.00")
    )

    try:
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
    except Exception:
        db.rollback()
        raise

    return {
        "id": new_account.id,
        "user_id": new_account.user_id,
        "account_type": new_account.account_type,
        "balance": str(new_account.balance)
    }
