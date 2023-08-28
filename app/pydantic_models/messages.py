# -*- coding: utf-8 -*-
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from app.database.models import SentEmail, SentSMS


class SentEmailPydantic(pydantic_model_creator(SentEmail)):
    pass


class SentSMSPydantic(pydantic_model_creator(SentSMS)):
    pass
