from api.database.models import User as User_DB_Model, Role as Role_DB_Model
from pydantic import BaseModel
from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator


class RolePydantic(pydantic_model_creator(Role_DB_Model)):
    pass

class UserPydantic(pydantic_model_creator(User_DB_Model)):
    pass

class UserInfoPydantic(UserPydantic):
    role_info: RolePydantic = None
