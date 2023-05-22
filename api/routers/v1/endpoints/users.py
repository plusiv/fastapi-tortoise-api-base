from api.security import auth, hashing, jwt_handler as jwt
from api.pydantic_models.user import UserInfoPydantic
from api.routers.v1.dependencies import token_dep

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated


router = APIRouter()

@router.get("/me", response_model=UserInfoPydantic)
async def get_user_info(token: token_dep):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-AUTHENTICATE": "Bearer"}
            )
    try:
        username = jwt.decode_username(token)
        if not username:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = await auth.get_user(username=username)
    if not user:
        raise credentials_exception
    return user


