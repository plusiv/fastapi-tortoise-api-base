# -*- coding: utf-8 -*-
from tortoise.contrib.pydantic.creator import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)

from app.database.models import Role, User


class RolePydantic(pydantic_model_creator(Role, name="Role")):
    pass


class UserPydantic(pydantic_model_creator(User, name="User")):
    pass


class UserPydanticList(pydantic_queryset_creator(User, name="UserList")):
    pass
