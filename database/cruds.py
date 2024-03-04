from typing import List, Optional
from fastapi import Query

from sqlalchemy.orm import Session
from sqlalchemy import and_, case, delete, distinct, or_, update
from sqlalchemy.future import select
from sqlalchemy.sql.expression import func

from .models import (
    User, 
    Account,
    Card,
    Transaction
    )
from schemas import (
    user as user_dto, 
    account as account_dto,
    card as card_dto,
    transaction as transaction_dto,
)

# Data Access Layer
class BaseCRUD:
    def __init__(self, db_session: Session):
        self.db_session = db_session

class UserCRUD(BaseCRUD):
    async def create_user(self, user: user_dto.UserCreate) -> User:
        new_user = User(**user.model_dump())
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
    
    async def read_user(self, user_id: int) -> User:
        q = await self.db_session.execute(select(User).where(User.id == user_id))
        return q.scalar()

class AccountCRUD(BaseCRUD):
    async def create_accounts(self, user_id:int, accounts: List[account_dto.AccountCreate]) -> List[Account]:
        new_accounts = [Account(user_id=user_id, **account.model_dump()) for account in accounts]

        self.db_session.add_all(new_accounts)
        await self.db_session.commit()

        return new_accounts
    
    async def all_accounts(self, user_id) -> List[Account]:
        q = await self.db_session.execute(select(Account.id).where(Account.user_id!=user_id))
        return q.scalars().all()
    
    async def read_accounts(self, user_id:int) -> List[Account]:
        q = await self.db_session.execute(select(Account).where(Account.user_id==user_id))
        return q.scalars().all()
    
    async def read_account(self, account_id:int) -> Account:
        q = await self.db_session.execute(select(Account).where(Account.id==account_id))
        return q.scalar()
    
    async def check_account(self, user_id: int, account_id: int) -> Account:
        q = await self.db_session.execute(select(Account).where(and_(Account.id==account_id, Account.user_id==user_id)))
        return q.scalar()
    

class CardCRUD(BaseCRUD):
    async def create_cards(self, cards: List[card_dto.CardCreate]) -> List[Card]:
        new_cards = [Card(**card.model_dump()) for card in cards]

        self.db_session.add_all(new_cards)
        await self.db_session.commit()

        return new_cards
        
    async def read_card(self, card_id:int):
        q = await self.db_session.execute(select(Card).where(Card.id == card_id))        
        return q.scalar()

class TransactionCRUD(BaseCRUD):
    async def create_transactions(self,
                                    transactions: List[transaction_dto.TransactionCreate]) -> List[Transaction]:
        new_trs = [Transaction(**transaction.model_dump()) for transaction in transactions]

        self.db_session.add_all(new_trs)
        await self.db_session.flush()

        return new_trs
    
    async def read_transactions(self, account_id:int) -> List[Transaction]:
        # pagination
        q = await self.db_session.execute(
            select(Transaction)\
            .where(or_(Transaction.sender_id==account_id, Transaction.receiver_id==account_id))\
            .order_by(-Transaction.created_at)
            .limit(15))
        
        return q.scalars().all()

