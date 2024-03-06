from typing import List, Union
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
    transfer as transfer_dto,
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
    
    async def all_accounts(self, user_id, my=False) -> List[Account]:
        if not my:
            q = await self.db_session.execute(select(Account.id).where(Account.user_id!=user_id))
        else:
            q = await self.db_session.execute(select(Account.id).where(Account.user_id==user_id))
        return q.scalars().all()
    
    async def read_accounts(self, user_id:int, 
                            show_option:Union[bool, None]=None, 
                            account_type:Union[int, None]=None) -> List[Account]:
        select_qry = select(Account).where(Account.user_id==user_id)
        if account_type != None:
            select_qry = select_qry.where(Account.account_type==account_type)
        if show_option != None:
            select_qry = select_qry.where(Account.is_show==show_option)
        q = await self.db_session.execute(select_qry)
        return q.scalars().all()
    
    async def read_account(self, account_id:int) -> Account:
        q = await self.db_session.execute(select(Account).where(Account.id==account_id))
        return q.scalar()
    
    async def check_account(self, user_id: int, account_id: int) -> Account:
        q = await self.db_session.execute(select(Account).where(and_(Account.id==account_id, Account.user_id==user_id)))
        return q.scalar()
    
    async def read_recents(self, account_ids:list[int]):
        q = await self.db_session.execute(
            select(Account.id, Account.is_favorite, func.max(Transaction.created_at))
            .join(Transaction, Account.id == Transaction.receiver_id)\
            .filter(Transaction.sender_id.in_(account_ids))\
            .group_by(Account.id)
            .order_by(-Account.is_favorite, -func.max(Transaction.created_at))\
            .limit(10))
        
        return [ {'id': a.id, 'is_favorite':a.is_favorite} for a in q.all()]
    
    async def toggle_show(self, account_id:int, is_show:bool):
        q = await self.db_session.execute(
            update(Account).where(Account.id==account_id).values(is_show=is_show)
        )

        return True

    async def toggle_favorite(self, account_id: int, is_favorite:bool):
        q = await self.db_session.execute(
            update(Account).where(Account.id==account_id).values(is_favorite=is_favorite)
        )

        return True
        
    

class CardCRUD(BaseCRUD):
    async def create_cards(self, cards: List[card_dto.CardCreate]) -> List[Card]:
        new_cards = [Card(**card.model_dump()) for card in cards]

        self.db_session.add_all(new_cards)
        await self.db_session.commit()

        return new_cards
    
    async def read_cards(self, user_id:int, from_date, to_date) -> List[Card]:
        q = await self.db_session.execute(
            select(Card, func.sum(Transaction.amount).label('amount'))
            .join(Account, Card.account_id==Account.id)
            .outerjoin(Transaction, Transaction.card_id==Card.id)
            .where(Account.user_id==user_id)
            .where(or_(Transaction.created_at==None, Transaction.created_at.between(from_date, to_date)))
            .group_by(Card.id))
        return [{'id': c.id, 'min_usage': c.min_usage, 'amount': amount, 'card_name': c.card_name} for c, amount in q.all()]
        
    async def read_card(self, card_id:int) -> Card:
        q = await self.db_session.execute(select(Card).where(Card.id == card_id))        
        return q.scalar()

class TransactionCRUD(BaseCRUD):
    async def create_transactions(self,
                                    transactions: List[transaction_dto.TransactionCreate]) -> List[Transaction]:
        new_trs = [Transaction(**transaction.model_dump()) for transaction in transactions]

        self.db_session.add_all(new_trs)
        await self.db_session.flush()

        return new_trs
    
    async def read_transactions(self, account_id:int, from_date:str=None, to_date:str=None, page:int=None) -> List[Transaction]:
        # pagination
        q = await self.db_session.execute(
            select(Transaction)
            .where(or_(Transaction.sender_id==account_id, Transaction.receiver_id==account_id))
            .where(Transaction.created_at.between(from_date, to_date) if from_date else Transaction.created_at < to_date)
            .order_by(-Transaction.created_at)
            .limit(15)
            .offset((page-1)*15 if page else 0))
        
        return q.scalars().all()
    
    async def read_monthly_used(self, account_ids:list[int], from_date:str, to_date:str) -> int:
        q = await self.db_session.execute(
            select(func.sum(Transaction.amount))
            .where(and_(Transaction.sender_id.in_(account_ids), from_date <= Transaction.created_at, to_date > Transaction.created_at)))
        
        return q.scalar()
    
    async def read_recents(self, account_ids:list[int]) -> List[Account]:
        # is_favorite
        q = await self.db_session.execute(
            select(Transaction, Account).join(Account, Account.id==Transaction.receiver_id)
            .where(and_(Transaction.sender_id.in_(account_ids)))
            .distinct()
            .limit(10))
        
        return q.scalars().all()


class TransferCRUD(BaseCRUD):
    async def make_transfer(self, transfer: transfer_dto.TransferCreate) -> Transaction:
        # make_transaction
        new_tran = Transaction(amount=transfer.amount, 
                               memo=transfer.memo, 
                               sender_id=transfer.sender_id, 
                               receiver_id=transfer.receiver_id,
                               is_fill=transfer.is_fill)

        self.db_session.add(new_tran)
        await self.db_session.flush()
        # update
        await self.db_session.execute(
            update(Account)
            .where(Account.id==transfer.sender_id)
            .values(balance=transfer.sender_balance))
        await self.db_session.execute(
            update(Account)
            .where(Account.id==transfer.receiver_id)
            .values(balance=transfer.receiver_balance))
        
        return new_tran
        