# -*- coding: utf-8 -*-
from app.pydantic_models.todos import (
    TodoPydantic,
    TodoPydanticList,
    TodoPydanticIn,
    TodoStatusPydantic,
    TodoStatusPydanticIn,
    TodoStatusPydanticList,
)
from app.pydantic_models.users import UserPydanticList
from app.routers.v1.dependencies import current_user, authorized_todo_user
from app.database.crud.todos import (
    create_user_todo,
    get_todo_ownership,
    get_user_todos,
    get_status,
    create_status,
    update_user_todo_status,
    add_user_to_todo,
    get_users_from_todo,
    remove_user_from_todo,
)

from fastapi import APIRouter, status, HTTPException


router = APIRouter()


@router.post("/", response_model=TodoPydantic)
async def post_todo(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo: TodoPydanticIn,
):
    if current_user:
        user_id = current_user.get("id")
        return (
            await create_user_todo(user_id=user_id, new_todo=todo)
            if isinstance(user_id, int)
            else None
        )


@router.get("/", response_model=TodoPydanticList)
async def get_todos(current_user: current_user, is_authorized: authorized_todo_user):
    user_id = current_user.get("id")
    return await get_user_todos(user_id=user_id) if isinstance(user_id, int) else None


@router.get("/{todo_id}", response_model=TodoPydantic)
async def get_todo(
    current_user: current_user, is_authorized: authorized_todo_user, todo_id: int
):
    user_id = current_user.get("id")
    return (
        await get_user_todos(user_id=user_id, todo_id=todo_id)
        if isinstance(user_id, int)
        else None
    )


@router.patch("/{todo_id}/{new_status}", response_model=TodoPydantic)
async def update_todo_status(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo_id: int,
    new_status_id: int,
):
    user_id = current_user.get("id")
    return (
        await update_user_todo_status(
            user_id=user_id, todo_id=todo_id, new_status_id=new_status_id
        )
        if isinstance(user_id, int)
        else None
    )


@router.post("/statuses", response_model=TodoStatusPydantic)
async def create_todo_status(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    status: TodoStatusPydanticIn,
):
    return await create_status(status)


@router.get("/statuses/{status_id}", response_model=TodoStatusPydanticList)
async def get_todo_status(current_user: current_user, status_id: int):
    return await get_status(status_id=status_id)


@router.post("/add-user/{todo_id}/{new_user_id}", response_model=TodoPydantic)
async def add_todo_user(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo_id: int,
    new_user_id: int,
):
    # Check if user is already in Todo
    if get_todo_ownership(todo_id=todo_id, user_id=new_user_id):
        return await add_user_to_todo(todo_id=todo_id, new_user_id=new_user_id)
    # Raise a forbidden status
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden: User does not have access to this Todo",
    )


@router.get("/{todo_id}/users", response_model=UserPydanticList)
async def get_todo_users(
    current_user: current_user, is_authorized: authorized_todo_user, todo_id: int
):
    return await get_users_from_todo(todo_id=todo_id)


@router.delete("/{todo_id}/{user_id}", response_model=TodoPydantic)
async def remove_todo_user(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo_id: int,
    user_id_to_romove: int,
):
    user_id = current_user.get("id")

    if user_id:
        # Check if user is already in Todo
        if get_todo_ownership(todo_id=todo_id, user_id=user_id):
            return await remove_user_from_todo(
                user_id=user_id_to_romove, todo_id=todo_id
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden: User does not have access to this Todo",
    )
