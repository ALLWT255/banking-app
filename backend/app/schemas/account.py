from typing import Literal
from pydantic import BaseModel, Field



class AccountCreate(BaseModel):
    account_type: Literal["checking", "savings"]
