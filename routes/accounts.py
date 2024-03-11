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
    return {'accounts': await account_crud.read_accounts(user.id, is_show, account_type)}

@router.get('/recent')
async def get_recent(
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
    account_type: Union[int, None] = None,
):
    if account_type not in [0, 2]: # 입출금, 연락처
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="account_type is not valid")

    # account_type으로 구분
    account_ids = await account_crud.all_accounts(user.id, my=True)
    return {'accounts': await account_crud.read_recents(account_ids, account_type, user.id)}

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
    # user.id가 다르면
    account = await account_crud.read_account(account_id)
    if account.user_id != user.id:
        account.balance = 0
    return {**account.to_dict(), 'is_own': account.user_id == user.id}

