from decimal import Decimal
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app.db.database import Base
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import process_transaction


@pytest.fixture
def transaction_db():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    owner = User(email="owner@example.test", password_hash="test-hash")
    other_user = User(email="other@example.test", password_hash="test-hash")
    session.add_all([owner, other_user])
    session.flush()

    account = Account(
        user_id=owner.id,
        account_type="checking",
        balance=Decimal("100.00"),
    )
    session.add(account)
    session.commit()

    yield session, owner.id, other_user.id, account.id

    session.close()
    engine.dispose()


def test_unverified_deposit_is_rejected_without_database_access():
    db = Mock(spec=Session)
    request = TransactionCreate(
        account_id=1,
        transaction_type="deposit",
        amount=Decimal("25.00"),
    )

    with pytest.raises(ValueError, match="trusted payment is verified"):
        process_transaction(db, request, current_user_id=1)

    db.execute.assert_not_called()
    db.add.assert_not_called()
    db.commit.assert_not_called()
    db.rollback.assert_not_called()


def test_withdrawal_still_updates_owned_account():
    db = Mock(spec=Session)
    account = Account(
        id=1,
        user_id=1,
        account_type="checking",
        balance=Decimal("100.00"),
    )
    db.execute.return_value.scalar_one_or_none.return_value = account
    request = TransactionCreate(
        account_id=1,
        transaction_type="withdrawal",
        amount=Decimal("25.00"),
    )

    transaction = process_transaction(db, request, current_user_id=1)

    assert account.balance == Decimal("75.00")
    assert transaction.transaction_type == "withdrawal"
    assert transaction.status == "completed"
    db.commit.assert_called_once()


def test_user_cannot_withdraw_from_another_users_account(transaction_db):
    db, owner_id, other_user_id, account_id = transaction_db
    request = TransactionCreate(
        account_id=account_id,
        transaction_type="withdrawal",
        amount=Decimal("25.00"),
    )

    with pytest.raises(ValueError, match="Account not found"):
        process_transaction(db, request, current_user_id=other_user_id)

    account = db.get(Account, account_id)
    transactions = db.scalars(select(Transaction)).all()
    assert account is not None
    assert account.user_id == owner_id
    assert account.balance == Decimal("100.00")
    assert transactions == []


def test_withdrawal_over_available_balance_makes_no_changes(transaction_db):
    db, owner_id, _, account_id = transaction_db
    request = TransactionCreate(
        account_id=account_id,
        transaction_type="withdrawal",
        amount=Decimal("100.01"),
    )

    with pytest.raises(ValueError, match="Insufficient funds"):
        process_transaction(db, request, current_user_id=owner_id)

    account = db.get(Account, account_id)
    transactions = db.scalars(select(Transaction)).all()
    assert account is not None
    assert account.balance == Decimal("100.00")
    assert transactions == []


def test_persistence_failure_rolls_back_balance_and_ledger(transaction_db):
    db, owner_id, _, account_id = transaction_db
    db.execute(text(
        """
        CREATE TRIGGER reject_transaction_insert
        BEFORE INSERT ON transactions
        BEGIN
            SELECT RAISE(ABORT, 'simulated persistence failure');
        END;
        """
    ))
    request = TransactionCreate(
        account_id=account_id,
        transaction_type="withdrawal",
        amount=Decimal("25.00"),
    )

    with pytest.raises(IntegrityError, match="simulated persistence failure"):
        process_transaction(db, request, current_user_id=owner_id)

    account = db.get(Account, account_id)
    transactions = db.scalars(select(Transaction)).all()
    assert account is not None
    assert account.balance == Decimal("100.00")
    assert transactions == []