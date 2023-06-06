# -*- coding: utf-8 -*-
from app.core.security import jwt_handler as jwt
from app.core.security.access_control import access_control as ac
from app.database.crud import users
from app.routers.v1 import ROUTE_PREFIX
from app.pydantic_models.users import UserInfoPydantic
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from casbin import Enforcer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{ROUTE_PREFIX}/login")
token_dep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: token_dep) -> UserInfoPydantic:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-AUTHENTICATE": "Bearer"},
    )
    try:
        username = jwt.decode_username(token)
        if not username:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = await users.get_user(username=username)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserInfoPydantic, Depends(get_current_user)]
):
    if current_user.disabled_at:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authorize_todo_operation(
    req: Request,
    enforcer: Enforcer = Depends(ac.get_todos_enforcer),
    user: UserInfoPydantic = Depends(get_current_active_user),
):
    sub = [role.slug for role in user.roles]
    obj = req.url.path
    act = req.method
    if not enforcer.enforce(sub, obj, act):
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Insufficient rights to perform this action",
        )


current_user = Annotated[UserInfoPydantic, Depends(get_current_active_user)]
authorized_todo_user = Annotated[UserInfoPydantic, Depends(authorize_todo_operation)]
