# -*- coding: utf-8 -*-
from tortoise.models import Model
from datetime import datetime
from app.database.models import Todo, TodoStatus
from app.pydantic_models.todo import TodoPydantic, TodoStatusPydantic


async def soft_delete(model: Model):
    model.disabled_at = datetime.now()
    await model.save()


async def serialize_todo(todo: Todo, todo_status: TodoStatus) -> TodoPydantic:
    todo_pydantic = await TodoPydantic.from_tortoise_orm(todo)
    todo_pydantic.status = await TodoStatusPydantic.from_tortoise_orm(todo_status)

    return todo_pydantic
