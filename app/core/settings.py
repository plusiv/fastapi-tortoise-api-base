from pydantic import BaseSettings, EmailStr, HttpUrl, ValidationError, Field, validator

ENV_PATH = ".env"


class Settings(BaseSettings):
    ENV: str = "development"

    DATABASE_TYPE: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: int | str
    TORTOISE_ORM: dict = None

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

    @validator("TORTOISE_ORM", always=True)
    def create_tortoise_config(cls, v, values, **kwargs):
        return {
            "connections": {
                "default": {
                    "engine": f"tortoise.backends.{values['DATABASE_TYPE']}",
                    "credentials": {
                        "host": values["DATABASE_HOST"],
                        "port": values["DATABASE_PORT"],
                        "user": values["DATABASE_USER"],
                        "password": values["DATABASE_PASSWORD"],
                        "database": values["DATABASE_NAME"]
                    }
                },
            },
            "apps": {
                "models": {"models": ["app.database.models", "aerich.models"], "default_connection": "default"},
            }
        }

    class Config:
        env_file = ENV_PATH
        case_sensitive = True


try:
    env = Settings()
    TORTOISE_ORM = env.TORTOISE_ORM
except ValidationError as e:
    print(f"A validation error has occoured in config file {ENV_PATH}: {e}")
    
