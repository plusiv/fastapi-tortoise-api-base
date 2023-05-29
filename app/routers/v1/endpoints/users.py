from app.pydantic_models.user import UserInfoPydantic
from app.routers.v1.dependencies import current_user

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated


router = APIRouter()

@router.get("/me", response_model=UserInfoPydantic)
def get_user_info(current_user: current_user):
    return current_user

