from pydantic import BaseModel
from typing import List

class TokenPydantic(BaseModel):
    access_token: str
    token_type: str = "bearer"
