
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import process_transaction
from app.core.security import get_current_user_id
from app.core.ai_security import check_sensitive_data
router = APIRouter()



@router.post("/transactions")
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
   current_user_id: int = Depends(get_current_user_id)
):
    try:
        transaction = process_transaction(
            db,
            transaction_data,
            current_user_id
        )

        return {
            "id": transaction.id,
            "account_id": transaction.account_id,
            "transaction_type": transaction.transaction_type,
            "amount": str(transaction.amount),
            "status": transaction.status
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
