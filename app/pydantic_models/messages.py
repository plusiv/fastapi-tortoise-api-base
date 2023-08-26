# -*- coding: utf-8 -*-
from app.database.models import SentEmail, SentSMS
from tortoise.contrib.pydantic.creator import pydantic_model_creator


class SentEmailPydantic(pydantic_model_creator(SentEmail)):
    pass


class SentSMSPydantic(pydantic_model_creator(SentSMS)):
    pass
