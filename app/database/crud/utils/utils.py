# -*- coding: utf-8 -*-
from tortoise.models import Model
from datetime import datetime
from app.database.models import User, Role, Todo, TodoStatus
from app.pydantic_models.todos import TodoPydantic, TodoStatusPydantic
from app.pydantic_models.users import UserInfoPydantic, RolePydantic


async def soft_delete(model: Model):
    model.disabled_at = datetime.now()
    await model.save()


async def serialize_todo(todo: Todo, todo_status: TodoStatus = None) -> TodoPydantic:
    todo_pydantic = await TodoPydantic.from_tortoise_orm(todo)
    if not todo_status:
        # Get last status
        todo_status = await todo.statuses.order_by("-created_at").first()

    todo_pydantic.status = await TodoStatusPydantic.from_tortoise_orm(todo_status)

    return todo_pydantic


async def serialize_user(user: User, roles: list[Role] = []) -> UserInfoPydantic:
    user_pydantic = await UserInfoPydantic.from_tortoise_orm(user)
    user_roles = roles
    if not roles:
        user_roles = await user.roles

    user_pydantic.roles = [
        await RolePydantic.from_tortoise_orm(user_role) for user_role in user_roles
    ]

    return user_pydantic
