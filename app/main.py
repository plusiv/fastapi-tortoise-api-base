# -*- coding: utf-8 -*-
from fastapi import FastAPI
from tortoise import exceptions as db_exception
from tortoise.contrib.fastapi import register_tortoise

from app.core.settings import TORTOISE_ORM, env, init_loggers, log
from app.routers.v1 import ROUTE_PREFIX as v1_prefix
from app.routers.v1 import api as v1

init_loggers()

app = FastAPI(title=env.APP_NAME, version=env.APP_VERSION)

try:
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        add_exception_handlers=True,
    )
except db_exception.ConfigurationError as e:
    log.error("A config error has occurred: {e}")
    raise e

except db_exception.DBConnectionError as e:
    log.error("A connection error has occurred: {e}")
    raise e

app.include_router(v1.router, prefix=v1_prefix)


# Health Check
@app.get("/ping", tags=["Health Check"])
async def ping():
    return "pong"
