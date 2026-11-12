
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.models.user import User



def process_transaction(
    db: Session,
    transaction_data: TransactionCreate,
    current_user_id: int
):
    if transaction_data.transaction_type == "deposit":
        raise ValueError(
            "Deposits are unavailable until a trusted payment is verified."
        )

    try:
        account = db.execute(
            select(Account)
            .where(
                Account.id == transaction_data.account_id,
                Account.user_id == current_user_id
            )
            .with_for_update()
        ).scalar_one_or_none()

        if account is None:
            raise ValueError("Account not found")

        amount = transaction_data.amount
        if transaction_data.transaction_type == "withdrawal":
            if account.balance < amount:
                raise ValueError("Insufficient funds")

            account.balance -= amount

        transaction = Transaction(
            account_id=account.id,
            transaction_type=transaction_data.transaction_type,
            amount=amount,
            status="completed"
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    except Exception:
        db.rollback()
        raise
