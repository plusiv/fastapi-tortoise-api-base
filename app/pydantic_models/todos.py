# -*- coding: utf-8 -*-
from app.database.models import Todo, TodoStatus
from tortoise.contrib.pydantic.creator import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)


class TodoStatusPydantic(pydantic_model_creator(TodoStatus, name="TodoStatus")):
    ...


class TodoStatusPydanticIn(
    pydantic_model_creator(
        TodoStatus,
        name="TodoStatusIn",
        exclude=("id", "modified_at", "disabled_at", "created_at"),
    )
):
    ...


class TodoStatusPydanticList(
    pydantic_queryset_creator(TodoStatus, name="TodoStatusList")
):
    ...


class TodoPydanticIn(
    pydantic_model_creator(
        Todo,
        name="TodoIn",
        exclude=("id", "modified_at", "disabled_at", "created_at"),
    )
):
    ...


class TodoPydantic(pydantic_model_creator(Todo, name="Todo")):
    ...


class TodoPydanticList(pydantic_queryset_creator(Todo, name="TodoList")):
    ...
