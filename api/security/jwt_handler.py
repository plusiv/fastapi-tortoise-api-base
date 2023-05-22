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
    encoded_jwt = jwt.encode(to_encode, env.get('SECRET_KEY'), algorithm=env.get('ALGORITHM'))
    return encoded_jwt

def decode_username(token) -> str | None:
    try:
        return jwt.decode(token, env.get('SECRET_KEY'), env.get('ALGORITHM')).get('sub')
    except JWTError:
        return
        
