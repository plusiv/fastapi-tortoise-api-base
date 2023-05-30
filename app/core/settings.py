# -*- coding: utf-8 -*-
import uvicorn
import logging
from pydantic import BaseSettings, EmailStr, HttpUrl, ValidationError

ENV_PATH = ".env"


class Settings(BaseSettings):
    ENV: str = "development"
    APP_NAME: str = "fastapi-tortoise"

    DATABASE_TYPE: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: int | str

    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SENDGRID_API_URL: HttpUrl = None
    SENDGRID_API_KEY: str = None
    SENDGRID_SENDER: EmailStr = None
    SENDGRID_NEW_USER_TEMPLATE_ID: str = None

    TWILIO_FROM_NUMBER: str = None
    TWILIO_API_URL: HttpUrl = None
    TWILIO_API_KEY: str = None

    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

    class Config:
        env_file = ENV_PATH
        case_sensitive = True


try:
    env = Settings()
except ValidationError as e:
    print(f"A validation error has occoured in config file {ENV_PATH}: {e}")

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": f"tortoise.backends.{env.DATABASE_TYPE}",
            "credentials": {
                "host": env.DATABASE_HOST,
                "port": env.DATABASE_PORT,
                "user": env.DATABASE_USER,
                "password": env.DATABASE_PASSWORD,
                "database": env.DATABASE_NAME,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_loggers() -> None:
    # create logger
    logger = logging.getLogger(env.APP_NAME)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = uvicorn.logging.DefaultFormatter(env.LOG_FORMAT)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


log = logging.getLogger(env.APP_NAME)
