# -*- coding: utf-8 -*-
from app.database.models import User, Role, Permission
from app.core.security.hashing import get_password_hash
import random
from faker import Faker


async def generate_seeders(number_of_users: int = 10, test_user: dict = None):
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
    sample_password = "sample"
    test_user = {"username": "test", "password": "test"} if not test_user else test_user
    for n in range(number_of_users):
        simple_profile = f.simple_profile()
        user = {
            "username": simple_profile.get("username")
            if n != 0
            else test_user["username"],
            "first_name": simple_profile.get("name").split(" ")[0],
            "last_name": simple_profile.get("name").split(" ")[1],
            "hashed_password": get_password_hash(
                sample_password if n != 0 else test_user["password"]
            ),
            "email": simple_profile.get("mail"),
            "sex": simple_profile.get("sex"),
            "birthdate": simple_profile.get("birthdate"),
        }
        user = await User.create(**user, role=random.choice(roles_list))
