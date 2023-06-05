# -*- coding: utf-8 -*-
from app.database.models import Todo, TodoStatus, User
from app.core.settings import env
from app.pydantic_models.todo import (
    TodoPydantic,
    TodoPydanticIn,
    TodoPydanticList,
    TodoStatusPydantic,
    TodoStatusPydanticIn,
    TodoStatusPydanticList,
)
from tortoise.exceptions import BaseORMException
from app.database.crud.utils import utils
from datetime import datetime


async def get_user_todos(
    user_id: int, todo_id: int = None
) -> TodoPydanticList | TodoPydantic:
    user = await User.get(id=user_id)
    todos = user.todos
    # last_status = await todos.statuses.order_by("-created_at").first()

    if todo_id:
        todos = await todos.filter(id=todo_id).first().prefetch_related("statuses")
        last_status = await todos.statuses.order_by("-created_at").first()
        todo_pydantic = await utils.serialize_todo(todos, last_status)
        return todo_pydantic

    await user.fetch_related("todos__statuses")
    todos_pydantic_list = []
    async for todo in user.todos:
        last_status = await todo.statuses.order_by("-created_at").first()
        todo_pydantic = await utils.serialize_todo(todo, last_status)
        todos_pydantic_list.append(todo_pydantic)

    return TodoPydanticList(__root__=todos_pydantic_list)


async def create_user_todo(user_id: int, todo: TodoPydanticIn) -> TodoPydantic:
    try:
        default_todo_status = await TodoStatus.get(slug=env.APP_TODO_DEFAULT_STATUS)
        todo_ = await Todo.create(**todo.dict())
        await todo_.users.add(await User.get(id=user_id))
        await todo_.statuses.add(default_todo_status)
        todo_ = await utils.serialize_todo(todo_, default_todo_status)
        return todo_

    except BaseORMException as e:
        # TODO: add logging
        print(e)
        return


async def update_user_todo_status(user_id: int, todo_id: int, new_status_id: int):
    new_todo_status = await TodoStatus.get(id=new_status_id)
    user = await User.get(id=user_id)
    todo = await user.todos.filter(id=todo_id).first()
    await todo.statuses.order_by("-created_at").first()

    last_status_traces = await todo.todo_status_traces.order_by("-created_at").first()
    last_status_traces.disabled_at = datetime.now()
    await last_status_traces.save()
    await todo.statuses.add(new_todo_status)

    return await utils.serialize_todo(todo, new_todo_status)


async def get_status(status_id: int) -> TodoStatusPydantic | TodoStatusPydanticList:
    if status_id:
        return await TodoStatusPydantic.from_tortoise_orm(
            await TodoStatus.get(id=status_id)
        )

    return await TodoStatusPydanticList.from_queryset(TodoStatus.all())


async def create_status(status: TodoStatusPydanticIn) -> TodoStatusPydantic:
    new_status = await TodoStatus.create(**status.dict())

    return await TodoStatusPydantic.from_tortoise_orm(new_status)
