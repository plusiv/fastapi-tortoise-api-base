# -*- coding: utf-8 -*-
from app.database.models import Todo as Todo_DB_Model, TodoStatus as TodoStatus_DB_Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel


class TodoStatusPydantic(
    pydantic_model_creator(TodoStatus_DB_Model, name="TodoStatus")
):
    ...


class TodoStatusPydanticIn(
    pydantic_model_creator(
        TodoStatus_DB_Model,
        name="TodoStatusIn",
        exclude=["id", "modified_at", "disabled_at", "created_at"],
    )
):
    ...


class TodoStatusPydanticList(
    pydantic_queryset_creator(TodoStatus_DB_Model, name="TodoStatusList")
):
    ...


class TodoPydanticIn(
    pydantic_model_creator(
        Todo_DB_Model,
        name="TodoIn",
        exclude=["id", "modified_at", "disabled_at", "created_at"],
    )
):
    ...


class TodoPydantic(pydantic_model_creator(Todo_DB_Model, name="Todo")):
    status: TodoStatusPydantic | None


class TodoPydanticList(BaseModel):
    __root__: list[TodoPydantic]
