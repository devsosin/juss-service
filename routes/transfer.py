from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import AccountCRUD, TransferCRUD
from database.dependencies import get_account_session, get_transfer_session

from typing import Annotated

from modules.dependencies import get_current_active_user
from schemas.transfer import TransferBase, TransferCreate

router = APIRouter(
    prefix="/transfer",
    tags=["transfer"],
    responses={404: {"description": "Not found"}},
)

@router.post('/')
async def make_transfer(
    user: Annotated[User, Depends(get_current_active_user)],
    transfer: TransferBase,
    account_crud: AccountCRUD = Depends(get_account_session),
    transfer_crud: TransferCRUD = Depends(get_transfer_session),
): # -> response dto
    if transfer.sender_id == transfer.receiver_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Same Account")
    
    # check_account로 계좌 확인
    send_account = await account_crud.check_account(user.id, transfer.sender_id)
    if not send_account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not Authorized",
            headers={"WWW-Authenticate": "Bearer"})

    # 계좌 잔액 확인
    if send_account.balance < transfer.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient Balance")

    # 받는 계좌 확인 -> 본인 계좌면 fill
    recv_account = await account_crud.read_account(transfer.receiver_id)
    if not recv_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Receiver Not Found")

    is_fill = False
    if recv_account.user_id == user.id:
        is_fill = True
    
    return await transfer_crud.make_transfer(
        TransferCreate(**transfer.model_dump(), 
                       is_fill=is_fill, 
                       sender_balance=send_account.balance - transfer.amount, 
                       receiver_balance=recv_account.balance + transfer.amount))
    