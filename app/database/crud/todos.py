# -*- coding: utf-8 -*-
from tortoise.contrib.pydantic.base import PydanticListModel, PydanticModel

from app.core.settings import env
from app.database.models import Todo, TodoStatus, User
from app.pydantic_models.todos import (
    TodoPydantic,
    TodoPydanticIn,
    TodoPydanticList,
    TodoStatusPydantic,
    TodoStatusPydanticIn,
    TodoStatusPydanticList,
)
from app.utils.utils import db_exceptions_handler


@db_exceptions_handler
async def get_user_todos(
    user_id: int | str, todo_id: int | None = None
) -> PydanticModel | PydanticListModel | None:
    """Returns a list of todos or a single todo if todo_id is provided.

    Arguments:
        user_id {int | str} -- User id
        todo_id {int | None} -- Todo id

    Returns:
        PydanticModel | PydanticListModel | None -- Todo or list of todos
    """
    filters = {"users__id": user_id}

    if todo_id:
        filters["id"] = todo_id

    todos = Todo.filter(**filters).prefetch_related("statuses")

    if todo_id:
        todos = await todos.first()
        if todos:
            return await TodoPydantic.from_tortoise_orm(todos)
        return None
    return await TodoPydanticList.from_queryset(todos)


@db_exceptions_handler
async def get_todo_ownership(user_id: int, todo_id: int) -> bool:
    """Returns True if user is owner of the Todo.

    Arguments:
        user_id {int} -- User id
        todo_id {int} -- Todo id

    Returns:
        bool -- True if user is owner of the Todo
    """
    todo = await Todo.filter(id=todo_id, users__id=user_id).exists()
    return True if todo else False


@db_exceptions_handler
async def create_user_todo(user_id: int, new_todo: TodoPydanticIn) -> PydanticModel:
    default_todo_status = await TodoStatus.get(slug=env.APP_TODO_DEFAULT_STATUS)
    # Create Todo
    todo = await Todo.create(**new_todo.model_dump())

    # Add TodoStatus to Todo
    await todo.statuses.add(default_todo_status)

    # Add User to Todo
    await todo.users.add(await User.get(id=user_id))

    return await TodoPydantic.from_tortoise_orm(todo)


@db_exceptions_handler
async def update_user_todo_status(
    user_id: int, todo_id: int, new_status_id: int
) -> PydanticModel | None:
    """Updates the status of a Todo

    Arguments:
        user_id {int} -- User id
        todo_id {int} -- Todo id
        new_status_id {int} -- New status id

    Returns:
        PydanticModel | None -- Updated Todo or None if not exists
    """
    new_todo_status = await TodoStatus.get(id=new_status_id)
    user = await User.get(id=user_id)
    todo = await Todo.filter(id=todo_id, users__in=[user]).first()

    if todo:
        last_status_trace = await todo.todo_status_traces.order_by(
            "-created_at"
        ).first()
        await last_status_trace.soft_delete() if last_status_trace else None
        await todo.statuses.add(new_todo_status)

        return await TodoPydantic.from_tortoise_orm(todo)

    return None


@db_exceptions_handler
async def get_status(status_id: int) -> PydanticModel | PydanticListModel:
    """Returns a list of statuses or a single status if status_id is provided.

    Arguments:
        status_id {int} -- Status id

    Returns:
        PydanticModel | PydanticListModel -- Status or list of statuses
    """
    if status_id:
        return await TodoStatusPydantic.from_tortoise_orm(
            await TodoStatus.get(id=status_id)
        )

    return await TodoStatusPydanticList.from_queryset(TodoStatus.all())


@db_exceptions_handler
async def create_status(status: TodoStatusPydanticIn) -> PydanticModel:
    """Creates a new status for Todos.

    Arguments:
        status {TodoStatusPydanticIn} -- Status data

    Returns:
        PydanticModel -- Created status
    """
    new_status = await TodoStatus.create(**status.model_dump())

    return await TodoStatusPydantic.from_tortoise_orm(new_status)


@db_exceptions_handler
async def add_user_to_todo(new_user_id: int, todo_id: int) -> PydanticModel | None:
    """Adds a user to a Todo.

    Arguments:
        new_user_id {int} -- User id
        todo_id {int} -- Todo id

    Returns:
        PydanticModel | None -- Updated Todo or None if not exists
    """
    todo = await Todo.filter(id=todo_id).first()

    if todo:
        await todo.users.add(await User.get(id=new_user_id))

    return None


@db_exceptions_handler
async def get_users_from_todo(todo_id: int) -> PydanticListModel | None:
    """Returns a list of users from a Todo.

    Arguments:
        todo_id {int} -- Todo id

    Returns:
        PydanticListModel | None -- List of users or None if not exists
    """
    todo = await Todo.filter(id=todo_id).first().prefetch_related("users")

    if todo:
        users = todo.users.all()
        return await PydanticListModel.from_queryset(users)

    return None


@db_exceptions_handler
async def remove_user_from_todo(user_id: int, todo_id) -> PydanticModel | None:
    """Removes a user from a Todo.

    Arguments:
        user_id {int} -- User id

    Returns:
        PydanticModel | None -- Updated Todo or None if not exists
    """

    todo = await Todo.filter(id=todo_id).first()

    if todo:
        await todo.users.remove(await User.get(id=user_id))
        return await TodoPydantic.from_tortoise_orm(todo)

    return None
