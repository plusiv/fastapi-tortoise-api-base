# -*- coding: utf-8 -*-
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from tortoise import Tortoise

from app.database.seeders import sample_seeders
from app.main import app

test_user = {"username": "test", "password": "test"}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"models": ["app.database.models"]},
        )
        await Tortoise.generate_schemas()

        await sample_seeders.generate_seeders(number_of_users=1, test_user=test_user)

        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
