from fastapi import HTTPException, Depends, status
from typing import Annotated

from database.models import User
from database.cruds import UserCRUD
from database.dependencies import get_user_session

from modules.utils import decode_token

from jose import JWTError

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_crud: UserCRUD = Depends(get_user_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        user_id:int = int(payload.get('user_id'))
        
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_crud.read_user(user_id)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user