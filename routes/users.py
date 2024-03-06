from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from database.models import User
from database.cruds import UserCRUD
from database.dependencies import get_user_session

from schemas import (
    user as user_dto,
)

from modules.utils import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token)

from typing import Annotated

from modules.dependencies import get_current_active_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router.post('/')
async def create_user(
    user: user_dto.UserCreate, 
    user_crud: UserCRUD = Depends(get_user_session),
):
    user = await user_crud.create_user(user)
    
    return {
        'access_token': create_access_token({'sub': str(user.id), 'user_id': str(user.id)}),
        'refresh_token': create_refresh_token({'sub': str(user.id), 'user_id': str(user.id)}),
        'token_type': 'Bearer'
    }

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_crud: UserCRUD = Depends(get_user_session),
) -> user_dto.Token:
    user = user_crud.read_user(form_data.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return user_dto.Token(access_token=access_token, token_type="bearer")

@router.get('/')
async def get_user(
    user: Annotated[User, Depends(get_current_active_user)]
):
    return user