from pydantic import BaseModel

## ACCOUNT
class AccountBase(BaseModel):
    account_type: int
    bank_name: str
    account_name: str
    account_number: str
    balance: int

class AccountCreate(AccountBase):
    ...

class Account(AccountBase):
    id: int

    is_show: bool
    is_favorite: bool

    class Config:
        from_attributes = True
