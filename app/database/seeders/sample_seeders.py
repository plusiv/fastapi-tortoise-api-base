# -*- coding: utf-8 -*-
import random

from faker import Faker

from app.core.security.hashing import get_password_hash
from app.core.settings import env
from app.database.models import Role, TodoStatus, User


async def generate_seeders(number_of_users: int = 10, test_user: dict | None = None):
    f = Faker(["es_ES"])

    # Insert Roles
    roles = ["viewer", "editor"]
    rolesModelList = [
        await Role.create(title=role_name.capitalize(), slug=role_name)
        for role_name in roles
    ]

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
        user = await User.create(**user)
        await user.roles.add(
            *random.sample(
                rolesModelList,
                len(rolesModelList) - 1 if len(rolesModelList) > 1 else 1,
            )
        )

    # Insert Default Todo Status
    todo_statuses = [env.APP_TODO_DEFAULT_STATUS, "in-progress", "done"]

    for todo_status in todo_statuses:
        await TodoStatus.create(
            name=todo_status.replace("-", " ").capitalize(), slug=todo_status
        )
