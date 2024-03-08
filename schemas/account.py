from typing import Union
from pydantic import BaseModel

## ACCOUNT
class AccountBase(BaseModel):
    account_type: int
    bank_name: str
    account_name: str
    account_number: str
    balance: int

class AccountCreate(AccountBase):
    is_show: Union[bool, None] = True
    ...

class Account(AccountBase):
    id: int

    is_favorite: bool

    class Config:
        from_attributes = True
