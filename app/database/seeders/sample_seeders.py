from app.database.models import User, Role, Permission
from app.core.security.hashing import get_password_hash
import random
from faker import Faker


async def run():
    f = Faker(["es_ES"])

    # Insert Roles
    roles = {
        "viewer": ["view"],
        "editor": ["view", "update"],
        "admin": ["view", "add", "update", "delete"],
    }

    roles_list = []
    for role_name in roles:
        role = await Role.create(title=role_name.capitalize(), slug=role_name)

        # Insert Permission
        permissions_list = []
        for permission_name in roles.get(role_name):
            permission = await Permission.get_or_create(
                title=permission_name.capitalize(), slug=permission_name
            )
            permissions_list.append(permission[0])

        roles_list.append(role)
        await role.permission.add(*permissions_list)

    # Insert Users
    NUMBER_OF_USERS = 10
    for _ in range(NUMBER_OF_USERS):
        simple_profile = f.simple_profile()
        user = {
            "username": simple_profile.get("username"),
            "first_name": simple_profile.get("name").split(" ")[0],
            "last_name": simple_profile.get("name").split(" ")[1],
            "hashed_password": get_password_hash("sample"),
            "email": simple_profile.get("mail"),
            "sex": simple_profile.get("sex"),
            "birthdate": simple_profile.get("birthdate"),
        }
        user = await User.create(**user, role=random.choice(roles_list))
