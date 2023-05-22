from api.database.models import User as User_DB_model
from pydantic import BaseModel
from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator


class User(pydantic_model_creator(User_DB_model)):
    pass
