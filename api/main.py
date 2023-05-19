from . import config as env
from .security import auth, hashing, jwt_handler as jwt
from .models import User, Token 
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


DATABASE_URL = f"{env['DATABASE_TYPE']}://{env['DATABASE_USER']}:{env['DATABASE_USER']}@{env['DATABASE_HOST']}/{env['DATABASE_NAME']}"
app = FastAPI()

# Health Check
@app.get("/ping")
async def ping():
    return "pong"

@app.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Incorrect username or password",
                headers={"WWW-AUTHENTICATE": "Bearer"}
                )
    access_token_expires = timedelta(minutes=env["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = jwt.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer").dict()

#register_tortoise(
#    app,
#    db_url=DATABASE_URL,
#    modules={"models": ["api.database.models"]},
#    generate_schemas=True,
#    add_exception_handlers=True,
#)


