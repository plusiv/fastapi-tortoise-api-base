from api.routers.v1 import ROUTE_PREFIX
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{ROUTE_PREFIX}/login")
token_dep = Annotated[str, Depends(oauth2_scheme)]
