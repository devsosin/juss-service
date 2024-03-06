from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import AccountCRUD, TransactionCRUD
from database.dependencies import get_account_session, get_transaction_session

from typing import Annotated, Union

from modules.dependencies import get_current_active_user

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)

# 이번 달 쓴 금액
@router.get('/used')
async def get_month_used(
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
    transaction_crud: TransactionCRUD = Depends(get_transaction_session),
):
    dt_now = datetime.now()
    from_date = datetime(dt_now.year, dt_now.month, 1)
    to_date = datetime(dt_now.year, dt_now.month+1, 1)
    if dt_now.month == 12:
        to_date = datetime(dt_now.year+1, 1, 1)

    account_ids = await account_crud.all_accounts(user.id, my=True)
    return await transaction_crud.read_monthly_used(account_ids, from_date, to_date)

@router.get('/topay')
async def get_to_pay(
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
    transaction_crud: TransactionCRUD = Depends(get_transaction_session),
):
    dt_now = datetime.now()
    if dt_now.day < 16:
        from_date = datetime(dt_now.year, dt_now.month-1, 15)
        to_date = datetime(dt_now.year, dt_now.month, 15)
    else:
        from_date = datetime(dt_now.year, dt_now.month, 15)
        to_date = datetime(dt_now.year, dt_now.month+1, 15)
        if dt_now.month == 12:
            to_date = datetime(dt_now.year+1, 1, 15)
    account_ids = await account_crud.all_accounts(user.id, my=True)
    return await transaction_crud.read_monthly_used(account_ids, from_date, to_date)

@router.get('/{account_id}')
async def get_transactions(
    account_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
    transaction_crud: TransactionCRUD = Depends(get_transaction_session),
    from_date: Union[str, None] = None,
    to_date: Union[str, None] = None,
    page: Union[int, None] = None,
): 
    if from_date and to_date:
        try:
            from_date = datetime.strptime(from_date, '%y%m%d') 
            to_date = datetime.strptime(to_date, '%y%m%d') + timedelta(days=1)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="from_date and to_date is not valid")
    else:
        to_date = datetime.now() + timedelta(days=1)

    # 계좌 당위성 확인
    if not await account_crud.check_account(user.id, account_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not Authorized",
            headers={"WWW-Authenticate": "Bearer"})
    
    return await transaction_crud.read_transactions(account_id, from_date, to_date, page)
