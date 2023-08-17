# -*- coding: utf-8 -*-
import uvicorn.logging as uvicorn_logging
import logging
from pydantic import EmailStr, HttpUrl, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = ".env"


class Settings(BaseSettings):
    ENV: str = "development"
    APP_NAME: str = "fastapi-tortoise-api-base"
    APP_VERSION: str = "0.1.0"
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"
    APP_TODO_DEFAULT_STATUS: str = "not-started"

    DATABASE_TYPE: str = "mysql"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "sample"
    DATABASE_HOST: str = "localhost"
    DATABASE_NAME: str = "database"
    DATABASE_PORT: int | str = 3306

    ACCESS_TOKEN_SECRET_KEY: str = "secret_sample"
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SENDGRID_API_URL: HttpUrl | None = None
    SENDGRID_API_KEY: str | None = None
    SENDGRID_SENDER: EmailStr | None = None
    SENDGRID_NEW_USER_TEMPLATE_ID: str = ""

    TWILIO_FROM_NUMBER: str | None = None
    TWILIO_API_URL: HttpUrl | None = None
    TWILIO_API_KEY: str | None = None

    model_config = SettingsConfigDict(case_sensitive=True, env_file=ENV_PATH)


env = None

try:
    env = Settings()

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

    SENDGRID_API_HEADERS = {
        "Authorization": f"Bearer {env.SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }

    SENDGRID_API_JSON_DATA_TEMPLATE = {
        "from": {
            "email": env.SENDGRID_SENDER,
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": "",
                    },
                ],
                "dynamic_template_data": {},
            },
        ],
        "template_id": "",
    }

    logger_name = env.APP_NAME if env else "logger"

    def init_loggers() -> None:
        # create logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = uvicorn_logging.DefaultFormatter(env.LOG_FORMAT if env else "")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    log = logging.getLogger(logger_name)

except ValidationError as e:
    print(f"A validation error has occoured in config file {ENV_PATH}: {e}")
