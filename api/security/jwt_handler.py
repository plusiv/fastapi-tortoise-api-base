from datetime import datetime, timedelta
from jose import JWTError, jwt
from api import env

def create_access_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=int(env["ACCESS_TOKEN_EXPIRE_MINUTES"]))
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env['SECRET_KEY'], algorithm=env['ALGORITHM'])
    return encoded_jwt
