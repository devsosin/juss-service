from pydantic import BaseModel
from typing import Union

## Transfer
class TransferBase(BaseModel):
    sender_id: int
    receiver_id: int
    amount: int
    memo: Union[str, None] = None

class TransferCreate(TransferBase):
    is_fill: bool
    sender_balance: int
    receiver_balance: int
