
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    account_id: int = Field(gt=0)

    transaction_type: Literal["deposit", "withdrawal"]

    amount: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2
    )
