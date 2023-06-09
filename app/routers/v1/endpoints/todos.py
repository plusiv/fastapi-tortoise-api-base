# -*- coding: utf-8 -*-
from app.pydantic_models.todos import (
    TodoPydantic,
    TodoPydanticList,
    TodoPydanticIn,
    TodoStatusPydantic,
    TodoStatusPydanticIn,
    TodoStatusPydanticList,
)
from app.pydantic_models.users import UserInfoPydanticList
from app.routers.v1.dependencies import current_user, authorized_todo_user
from app.database.crud.todos import (
    create_user_todo,
    get_user_todos,
    get_status,
    create_status,
    update_user_todo_status,
    add_user_to_todo,
    get_users_from_todo,
    remove_user_from_todo,
)

from fastapi import APIRouter


router = APIRouter()


@router.post("/", response_model=TodoPydantic)
async def post_todo(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo: TodoPydanticIn,
):
    return await create_user_todo(user_id=current_user.id, todo=todo)


@router.get("/", response_model=TodoPydanticList)
async def get_todos(current_user: current_user, is_authorized: authorized_todo_user):
    return await get_user_todos(user_id=current_user.id)


@router.get("/{todo_id}", response_model=TodoPydantic)
async def get_todo(
    current_user: current_user, is_authorized: authorized_todo_user, todo_id: int
):
    return await get_user_todos(user_id=current_user.id, todo_id=todo_id)


@router.patch("/{todo_id}/{new_status}", response_model=TodoPydantic)
async def update_todo_status(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo_id: int,
    new_status_id: int,
):
    return await update_user_todo_status(
        user_id=current_user.id, todo_id=todo_id, new_status_id=new_status_id
    )


@router.post("/statuses", response_model=TodoStatusPydantic)
async def create_todo_status(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    status: TodoStatusPydanticIn,
):
    return await create_status(status)


@router.get("/statuses", response_model=TodoStatusPydanticList)
async def get_todo_statuses(
    current_user: current_user, is_authorized: authorized_todo_user, todo_id: int
):
    return await get_status()


@router.get("/statuses/{status_id}", response_model=TodoStatusPydanticList)
async def get_todo_status(current_user: current_user, status_id: int):
    return await get_status(status_id=status_id)


@router.post("/add-user/{todo_id}/{new_user_id}", response_model=TodoPydantic)
async def add_todo_user(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo_id: int,
    user_id: int | str,
):
    return await add_user_to_todo(
        owner_user_id=current_user.id, user_id=user_id, todo_id=todo_id
    )


@router.get("/{todo_id}/users", response_model=UserInfoPydanticList)
async def get_todo_users(
    current_user: current_user, is_authorized: authorized_todo_user, todo_id: int
):
    return await get_users_from_todo(owner_user_id=current_user.id, todo_id=todo_id)


@router.delete("/{todo_id}/{user_id}", response_model=TodoPydantic)
async def remove_todo_user(
    current_user: current_user,
    is_authorized: authorized_todo_user,
    todo_id: int,
    user_id: int | str,
):
    return await remove_user_from_todo(
        owner_user_id=current_user.id, user_id=user_id, todo_id=todo_id
    )
