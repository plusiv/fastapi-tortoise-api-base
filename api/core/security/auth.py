from api.database.models import User, Role
from api.pydantic_models.user import UserPydantic, RolePydantic, UserInfoPydantic
from api.core.security.hashing import verify_password
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

async def get_user(username: str) -> UserInfoPydantic | None:
    user_futures = User.get_or_none(username=username)
    user_values = await user_futures.values()

    if user_values:
        user_with_releated = await user_futures.prefetch_related('role')
        role_pydantic = await RolePydantic.from_tortoise_orm(user_with_releated.role)

        user_pydantic = await UserInfoPydantic.from_tortoise_orm( await user_futures )
        user_pydantic.role_info = role_pydantic
        return user_pydantic

    return None
