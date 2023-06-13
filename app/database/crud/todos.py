# -*- coding: utf-8 -*-
from app.database.models import Todo, TodoStatus, User
from app.core.settings import env
from app.pydantic_models.todos import (
    TodoPydantic,
    TodoPydanticIn,
    TodoPydanticList,
    TodoStatusPydantic,
    TodoStatusPydanticIn,
    TodoStatusPydanticList,
)
from app.pydantic_models.users import UserInfoPydanticList
from app.database.crud.utils import utils
from app.utils.utils import db_exceptions_handler


@db_exceptions_handler
async def get_user_todos(
    user_id: int | str, todo_id: int = None
) -> TodoPydanticList | TodoPydantic:
    user = await User.get(id=user_id)
    todos = user.todos
    # last_status = await todos.statuses.order_by("-created_at").first()

    if todo_id:
        todos = await todos.filter(id=todo_id).first().prefetch_related("statuses")
        todo_pydantic = await utils.serialize_todo(todos)
        return todo_pydantic

    await user.fetch_related("todos__statuses")
    todos_pydantic_list = []
    async for todo in user.todos:
        todo_pydantic = await utils.serialize_todo(todo)
        todos_pydantic_list.append(todo_pydantic)

    return TodoPydanticList(__root__=todos_pydantic_list)


@db_exceptions_handler
async def create_user_todo(user_id: int | str, todo: TodoPydanticIn) -> TodoPydantic:
    default_todo_status = await TodoStatus.get(slug=env.APP_TODO_DEFAULT_STATUS)
    todo_ = await Todo.create(**todo.dict())
    await todo_.users.add(await User.get(id=user_id))
    await todo_.statuses.add(default_todo_status)
    todo_ = await utils.serialize_todo(todo_, default_todo_status)
    return todo_


@db_exceptions_handler
async def update_user_todo_status(user_id: int | str, todo_id: int, new_status_id: int):
    new_todo_status = await TodoStatus.get(id=new_status_id)
    user = await User.get(id=user_id)
    todo = await user.todos.filter(id=todo_id).first()

    last_status_trace = await todo.todo_status_traces.order_by("-created_at").first()
    await utils.soft_delete(last_status_trace)
    await todo.statuses.add(new_todo_status)

    return await utils.serialize_todo(todo, new_todo_status)


@db_exceptions_handler
async def get_status(status_id: int) -> TodoStatusPydantic | TodoStatusPydanticList:
    if status_id:
        return await TodoStatusPydantic.from_tortoise_orm(
            await TodoStatus.get(id=status_id)
        )

    return await TodoStatusPydanticList.from_queryset(TodoStatus.all())


@db_exceptions_handler
async def create_status(status: TodoStatusPydanticIn) -> TodoStatusPydantic:
    new_status = await TodoStatus.create(**status.dict())

    return await TodoStatusPydantic.from_tortoise_orm(new_status)


@db_exceptions_handler
async def add_user_to_todo(
    owner_user_id: int | str, user_id: int | str, todo_id: int
) -> TodoPydantic:
    user = await User.get(id=owner_user_id)
    todo = await user.todos.filter(id=todo_id).first()

    await todo.users.add(await User.get(id=user_id))
    return await utils.serialize_todo(todo)


@db_exceptions_handler
async def get_users_from_todo(
    owner_user_id: int | str, todo_id: int
) -> UserInfoPydanticList:
    user = await User.get(id=owner_user_id)
    todo = await user.todos.filter(id=todo_id).first()

    user_info_list = [await utils.serialize_user(user) async for user in todo.users]

    return UserInfoPydanticList(__root__=user_info_list)


@db_exceptions_handler
async def remove_user_from_todo(
    owner_user_id: int | str, user_id: int | str, todo_id
) -> TodoPydantic:
    user = await User.get(id=user_id)
    todo = await user.todos.filter(id=todo_id).first()

    await todo.users.remove(user)

    return await utils.serialize_todo(todo)
