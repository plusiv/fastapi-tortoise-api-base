from api.database.models import SentEmail
from pydantic import BaseModel
from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator


class SentEmailPydantic(pydantic_model_creator(SentEmail)):
    pass

