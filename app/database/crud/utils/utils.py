# -*- coding: utf-8 -*-
from tortoise.models import Model
from datetime import datetime


def soft_delete(model: Model):
    model.disabled_at = datetime.now()
    await model.save()
