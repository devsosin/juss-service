# 데이터 생성
import random
from fastapi import APIRouter, HTTPException, Depends, status

from database.cruds import AccountCRUD, CardCRUD, TransactionCRUD
from database.dependencies import get_account_session, get_card_session, get_transaction_session

from database.models import User

from typing import Annotated

from modules.dependencies import get_current_active_user
from modules.generator import make_accounts, make_cards, make_transactions
from schemas.account import AccountCreate
from schemas.card import CardCreate
from schemas.transaction import TransactionCreate

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)

@router.post('/')
async def create_data(
    user: Annotated[User, Depends(get_current_active_user)],
    account_crud: AccountCRUD = Depends(get_account_session),
    card_crud: CardCRUD = Depends(get_card_session),
    transaction_crud: TransactionCRUD = Depends(get_transaction_session),
):
    try:
        user_id = user.id
        other_accounts = await account_crud.all_accounts(user_id)

        rd_accounts = [AccountCreate(**a) for a in make_accounts()]
        accounts = await account_crud.create_accounts(user_id, rd_accounts)
        accounts.pop()

        random.shuffle(accounts)
        rd_cards = [CardCreate(**c, account_id=accounts[i].id) for i, c in enumerate(make_cards())]
        cards = await card_crud.create_cards(rd_cards)

        accounts = [a.to_dict() for a in accounts]
        # 계좌에 카드 등록
        for card in cards:
            for account in accounts:
                if account['id'] == card.account_id:
                    account['card_id'] = card.id

        if other_accounts:
            # cards[0].account_id 이거에 따라서 card_id 선택하거나 선택하지 않을 수 있도록
            rd_trs = [TransactionCreate(**tr) for tr in make_transactions(accounts, other_accounts)]
            trs = await transaction_crud.create_transactions(rd_trs)
            
        return {
            'msg': "data created"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
            # headers={"WWW-Authenticate": "Bearer"})
    