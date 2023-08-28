# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.pydantic_models.users import UserPydantic
from app.routers.v1.dependencies import current_user

router = APIRouter()


@router.get("/me", response_model=UserPydantic)
async def get_user_info(current_user: current_user):
    return current_user
