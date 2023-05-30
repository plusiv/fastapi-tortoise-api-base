from pydantic import BaseModel


class TokenPydantic(BaseModel):
    access_token: str
    token_type: str = "bearer"
