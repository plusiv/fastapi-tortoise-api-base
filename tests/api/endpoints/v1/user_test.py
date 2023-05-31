# -*- coding: utf-8 -*-

from tortoise import Tortoise

from app.main import app
from app.database.models import User, Role, Permission
from app.core.security import hashing
from faker import Faker
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

import pytest
import random

sample_user = {"username": "user", "password": "sample"}

f = Faker(["es_ES"])
simple_profile = f.simple_profile()
user_data = {
    "username": sample_user.get("username"),
    "first_name": simple_profile.get("name").split(" ")[0],
    "last_name": simple_profile.get("name").split(" ")[1],
    "hashed_password": hashing.get_password_hash(sample_user.get("password")),
    "email": simple_profile.get("mail"),
    "sex": simple_profile.get("sex"),
    "birthdate": simple_profile.get("birthdate"),
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        # initializer(["app.database.models"],db_url="sqlite://:memory:" )  # Initialize Tortoise ORM

        await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"models": ["app.database.models"]},
        )
        await Tortoise.generate_schemas()

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

        await User.create(**user_data, role=random.choice(roles_list))

        # with TestClient(app) as client:
        #    yield client
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c

        # finalizer()


@pytest.mark.anyio
async def test_user_login(client):
    data = {
        "username": sample_user.get("username"),
        "password": sample_user.get("password"),
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = await client.post("/api/v1/login", data=data, headers=headers)

    assert response.status_code == 200
