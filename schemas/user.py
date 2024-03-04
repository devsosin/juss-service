from pydantic import BaseModel
from typing import Union

## USER
class UserBase(BaseModel):
    ...

class UserCreate(UserBase):
    ...

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

## TOKEN
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Union[int, None] = None
