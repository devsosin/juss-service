from fastapi import APIRouter, HTTPException, Depends, status

from database.models import User
from database.cruds import CardCRUD
from database.dependencies import get_card_session

from typing import Annotated

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
): # -> response dto
    
    return await card_crud.read_accounts(user.id)

@router.get('/{card_id}')
async def get_card(
    card_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    card_crud: CardCRUD = Depends(get_card_session),
):
    # if not [account for account in user.accounts if account.id == account_id]:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="User is not Authorized",
    #         headers={"WWW-Authenticate": "Bearer"})
    
    return await card_crud.read_card(card_id)