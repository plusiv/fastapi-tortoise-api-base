# -*- coding: utf-8 -*-
from app.database.models import User as User_DB_Model, Role as Role_DB_Model
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel


class RolePydantic(pydantic_model_creator(Role_DB_Model)):
    pass


class UserPydantic(pydantic_model_creator(User_DB_Model)):
    pass


class UserInfoPydantic(UserPydantic):
    roles: list[RolePydantic] = None


class UserInfoPydanticList(BaseModel):
    __root__: list[UserInfoPydantic]
