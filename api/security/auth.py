from api.database.models import User
from api.security.hashing import verify_password

async def authenticate_user(username: str, password: str)->bool:
    hashed_password = await User.get_or_none(username=username).values('hashed_password')
    return verify_password(plain_password=password, hashed_password=hashed_password.get('hashed_password')) if hashed_password else False
