from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import AccountCRUD
from database.dependencies import get_account_session

from typing import Annotated, Union

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
    is_show: Union[bool, None] = None,
    account_type: Union[int, None] = None,
):
    return await account_crud.read_accounts(user.id, is_show, account_type)

@router.get('/recent')
async def get_recent(
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
):
    account_ids = await account_crud.all_accounts(user.id, my=True)
    return await account_crud.read_recents(account_ids)

@router.put('/show/{account_id}')
async def change_show(
    account_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
):
    account = await account_crud.check_account(user.id, account_id)
    return await account_crud.toggle_show(account_id, not account.is_show)

@router.put('/favorite/{account_id}')
async def change_favorite(
    account_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
):
    account = await account_crud.read_account(account_id)
    return await account_crud.toggle_favorite(account_id, not account.is_favorite)

@router.get('/{account_id}')
async def get_account(
    account_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
):    
    return await account_crud.check_account(user.id, account_id)

