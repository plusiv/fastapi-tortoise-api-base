# -*- coding: utf-8 -*-
from app.pydantic_models.todo import (
    TodoPydantic,
    TodoPydanticList,
    TodoPydanticIn,
    TodoStatusPydantic,
    TodoStatusPydanticIn,
    TodoStatusPydanticList,
)
from app.routers.v1.dependencies import current_user
from app.database.crud.todos import (
    create_user_todo,
    get_user_todos,
    get_status,
    create_status,
    update_user_todo_status,
)

from fastapi import APIRouter


router = APIRouter()


@router.post("/", response_model=TodoPydantic)
async def post_todo(current_user: current_user, todo: TodoPydanticIn):
    return await create_user_todo(user_id=current_user.id, todo=todo)


@router.get("/", response_model=TodoPydanticList)
async def get_todos(current_user: current_user):
    return await get_user_todos(user_id=current_user.id)


@router.get("/{todo_id}", response_model=TodoPydantic)
async def get_todo(current_user: current_user, todo_id: int):
    return await get_user_todos(user_id=current_user.id, todo_id=todo_id)


@router.patch("/{todo_id}/{new_status}", response_model=TodoPydantic)
async def update_todo_status(
    current_user: current_user, todo_id: int, new_status_id: int
):
    return await update_user_todo_status(
        user_id=current_user.id, todo_id=todo_id, new_status_id=new_status_id
    )


@router.post("/statuses", response_model=TodoStatusPydantic)
async def create_todo_status(current_user: current_user, status: TodoStatusPydanticIn):
    return await create_status(status)


@router.get("/statuses", response_model=TodoStatusPydanticList)
async def get_todo_statuses(current_user: current_user, todo_id: int):
    return await get_status()


@router.get("/statuses/{status_id}", response_model=TodoStatusPydanticList)
async def get_todo_status(current_user: current_user, status_id: int):
    return await get_status(status_id=status_id)
