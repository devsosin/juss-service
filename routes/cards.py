from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import CardCRUD
from database.dependencies import get_card_session

from typing import Annotated, Union

from modules.dependencies import get_current_active_user

router = APIRouter(
    prefix="/card",
    tags=["card"],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
async def get_cards(
    user: Annotated[User, Depends(get_current_active_user)],
    card_crud: CardCRUD = Depends(get_card_session),
    ym: Union[str, None] = None,
):
    if ym == None:
        now = datetime.now()
    else:
        try:
            now = datetime.strptime(ym, '%Y%m')
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ym format is not valid")

    from_date = datetime(now.year, now.month, 1)
    to_date = datetime(now.year+1, now.month+1, 1)
    if now.month == 12:
        to_date = datetime(now.year+1, 1, 1)

    return await card_crud.read_cards(user.id, from_date, to_date)

@router.get('/{card_id}')
async def get_card(
    card_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    card_crud: CardCRUD = Depends(get_card_session),
):
    # if not [account for account in user.accounts if account.id == account_id]:

    
    return await card_crud.read_card(card_id)