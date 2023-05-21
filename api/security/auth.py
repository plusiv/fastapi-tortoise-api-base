from api.database.models import User
from api.security.hashing import verify_password
from datetime import datetime

async def authenticate_user(username: str, password: str)->bool:
    user = await User.get_or_none(username=username)

    # Avoid password verification if user is None
    hashed_password = user.hashed_password if user else None

    if hashed_password:
        if verify_password(plain_password=password, hashed_password=hashed_password):
            user.last_login = datetime.now()
            await user.save()
            return True
    return False
