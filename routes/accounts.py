from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import AccountCRUD
from database.dependencies import get_account_session

from schemas import (
    user as user_dto,
)

from typing import Annotated

from modules.dependencies import get_current_active_user

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
async def get_accounts(
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
): # -> response dto
    
    return await account_crud.read_accounts(user.id)

@router.get('/{account_id}')
async def get_account(
    account_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
):
    if not [account for account in user.accounts if account.id == account_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not Authorized",
            headers={"WWW-Authenticate": "Bearer"})
    
    return await account_crud.read_account(account_id)