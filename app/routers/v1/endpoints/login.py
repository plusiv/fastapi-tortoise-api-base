# -*- coding: utf-8 -*-
from app.core.security import jwt_handler as jwt
from app.database.crud.users import authenticate_user
from app.pydantic_models.tokens import TokenPydantic

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter()


@router.post("/login", response_model=TokenPydantic)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenPydantic:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-AUTHENTICATE": "Bearer"},
        )
    access_token = jwt.create_access_token(data={"sub": form_data.username})
    return TokenPydantic(access_token=access_token, token_type="bearer").dict()
