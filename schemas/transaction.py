from datetime import datetime
from pydantic import BaseModel
from typing import Union

## Transaction
class TransactionBase(BaseModel):
    receiver_id: int
    sender_id: int
    amount: int
    memo: str
    is_fill: bool
    card_id: Union[int, None]

class TransactionCreate(TransactionBase):
    created_at: Union[datetime, None]
    ...

class Transaction(TransactionBase):
    id: int

    is_show: bool
    is_favorite: bool

    class Config:
        from_attributes = True
