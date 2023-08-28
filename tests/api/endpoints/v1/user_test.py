# -*- coding: utf-8 -*-
import pytest
from fastapi import status

from tests.conftest import test_user


@pytest.mark.anyio
async def test_user_login(client):
    data = {
        "username": test_user.get("username"),
        "password": test_user.get("password"),
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = await client.post("/api/v1/login", data=data, headers=headers)

    assert response.status_code == status.HTTP_200_OK
