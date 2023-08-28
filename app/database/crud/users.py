# -*- coding: utf-8 -*-
from datetime import datetime

from tortoise.contrib.pydantic.base import PydanticModel

from app.core.security.hashing import verify_password
from app.database.models import User
from app.pydantic_models.users import UserPydantic
from app.utils.utils import db_exceptions_handler


@db_exceptions_handler
async def get_user(username: str) -> PydanticModel | None:
    user = await User.get_or_none(username=username).prefetch_related(
        "roles", "todos", "sent_emails", "sent_smss"
    )
    print(user)

    if user:
        user_pydantic = await UserPydantic.from_tortoise_orm(user)

        print(user_pydantic)
        return user_pydantic

    return None


@db_exceptions_handler
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
