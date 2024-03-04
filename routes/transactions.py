from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import AccountCRUD, TransactionCRUD
from database.dependencies import get_account_session, get_transaction_session

from schemas import (
    user as user_dto,
)

from typing import Annotated

from modules.dependencies import get_current_active_user

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)

@router.get('/{account_id}')
async def get_transactions(
    account_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
    transaction_crud: TransactionCRUD = Depends(get_transaction_session),
): # -> response dto
    # 계좌 당위성 확인
    if not await account_crud.check_account(user.id, account_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not Authorized",
            headers={"WWW-Authenticate": "Bearer"})
    
    return await transaction_crud.read_transactions(account_id)

@router.get('/')
async def get_account(
    user: Annotated[User, Depends(get_current_active_user)]
):
    # account info
    return user