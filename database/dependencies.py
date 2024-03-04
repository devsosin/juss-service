from .conn import async_session
from .cruds import (
    UserCRUD, 
    AccountCRUD,
    CardCRUD,
    TransactionCRUD
)

async def get_user_session():
    async with async_session() as session:
        async with session.begin():
            yield UserCRUD(session)

async def get_account_session():
    async with async_session() as session:
        async with session.begin():
            yield AccountCRUD(session)

async def get_card_session():
    async with async_session() as session:
        async with session.begin():
            yield CardCRUD(session)

async def get_transaction_session():
    async with async_session() as session:
        async with session.begin():
            yield TransactionCRUD(session)
