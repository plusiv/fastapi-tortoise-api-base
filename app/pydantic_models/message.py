from app.database.models import SentEmail, SentSMS
from pydantic import BaseModel
from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator


class SentEmailPydantic(pydantic_model_creator(SentEmail)):
    pass

class SentSMSPydantic(pydantic_model_creator(SentSMS)):
    pass
