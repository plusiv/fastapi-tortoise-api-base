# -*- coding: utf-8 -*-
from app.database.models import User
from app.database.crud.utils import utils
from app.pydantic_models.users import UserInfoPydantic
from app.core.security.hashing import verify_password
from datetime import datetime


async def get_user(username: str) -> UserInfoPydantic | None:
    user = await User.get_or_none(username=username)

    if user:
        user_pydantic = await utils.serialize_user(user)
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
