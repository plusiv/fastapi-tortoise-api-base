# -*- coding: utf-8 -*-
from app.database.models import User as User, Role
from tortoise.contrib.pydantic.creator import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)


class RolePydantic(pydantic_model_creator(Role, name="Role")):
    pass


class UserPydantic(pydantic_model_creator(User, name="User")):
    pass


class UserPydanticList(pydantic_queryset_creator(User, name="UserList")):
    pass
