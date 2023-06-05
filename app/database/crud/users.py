# -*- coding: utf-8 -*-
from app.database.models import User
from app.pydantic_models.user import UserInfoPydantic, RolePydantic
from app.core.security.hashing import verify_password
from datetime import datetime


async def get_user(username: str) -> UserInfoPydantic | None:
    user = await User.get_or_none(username=username)

    if user:
        user_roles = await user.roles
        user_roles_pydantic = [
            await RolePydantic.from_tortoise_orm(user_role) for user_role in user_roles
        ]
        user_pydantic = await UserInfoPydantic.from_tortoise_orm(user)
        user_pydantic.roles = user_roles_pydantic
        return user_pydantic

    return None


async def authenticate_user(username: str, password: str) -> bool:
    user = await User.get_or_none(username=username)

    if user:
        # Avoid password verification if user is None
        hashed_password = user.hashed_password
        if verify_password(plain_password=password, hashed_password=hashed_password):
            user.last_login = datetime.now()
            await user.save()
            return True
    return False
