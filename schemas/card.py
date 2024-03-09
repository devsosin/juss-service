from pydantic import BaseModel

## CARD
class CardBase(BaseModel):
    card_name: str
    min_usage: int
    account_id: int
    is_credit: bool

class CardCreate(CardBase):
    ...

class Card(CardBase):
    id: int

    is_show: bool
    is_favorite: bool

    class Config:
        from_attributes = True
