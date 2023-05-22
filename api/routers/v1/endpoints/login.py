from api.security import auth, hashing, jwt_handler as jwt
from api.pydantic_models.token import TokenPydantic

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter()

@router.post("/login", response_model=TokenPydantic)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-AUTHENTICATE": "Bearer"}
                )
    access_token = jwt.create_access_token(data={"sub": form_data.username})
    return TokenPydantic(access_token=access_token, token_type="bearer").dict()
