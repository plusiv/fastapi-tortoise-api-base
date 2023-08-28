# -*- coding: utf-8 -*-
# This file contains database models that satisfies basic needs. The length
# many of the standards used here has been taken from
# https://www.geekslop.com/technology-articles/2016/here-are-the-recommended-maximum-data-length-limits-for-common-database-and-programming-fields.
# Some fields like e-mail has been taken from its RFC like the RFC 3696 for
# e-mail standards.
from tortoise.models import Model
from tortoise import fields
from datetime import datetime
from enum import Enum


# Enums
class Sex(str, Enum):
    male = "M"
    female = "F"


# Helper Models
class TimestampMixin(Model):
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True)
    disabled_at = fields.DatetimeField(null=True)

    async def soft_delete(self):
        self.disabled_at = datetime.now()
        await self.save()


class Describable:
    description = fields.CharField(null=True, max_length=255)


class Message:
    sent_at = fields.DatetimeField(auto_now_add=True, null=True)


# Database Models
class User(TimestampMixin):
    username = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=320, unique=True)
    hashed_password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=70)
    last_name = fields.CharField(max_length=70)
    sex = fields.CharEnumField(Sex, null=True)
    birthdate = fields.DateField(null=True)
    last_login = fields.DatetimeField(null=True)

    # Relationships
    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField(
        "models.Role", related_name="users"
    )
    todos: fields.ManyToManyRelation["Todo"] = fields.ManyToManyField(
        "models.Todo", related_name="users"
    )

    class Meta:
        table = "user"

    class PydanticMeta:
        exclude = ("hashed_password",)
        backward_relations = False


class Role(TimestampMixin, Describable):
    title = fields.CharField(max_length=50)
    slug = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "role"


class SentEmail(Model, Describable, Message):
    email_subject = fields.CharField(max_length=150, null=True)
    from_email = fields.CharField(max_length=320)
    to_email = fields.CharField(max_length=320)
    template_name = fields.CharField(max_length=150, null=True)
    template_id = fields.CharField(max_length=50, null=True)

    # Relationships
    user = fields.ForeignKeyField("models.User", related_name="sent_emails")

    class Meta:
        table = "sent_email"

    class PydanticMeta:
        exclude = ["template_id"]


class SentSMS(Model, Describable, Message):
    # Max length based on Twilio number format.
    # see https://www.twilio.com/docs/voice/twiml/number#attributes
    from_sms = fields.CharField(max_length=11)
    to_sms = fields.CharField(max_length=11)

    # Max length based on Twilio recommendations.
    # see https://support.twilio.com/hc/en-us/articles/360033806753-Maximum-Message-Length-with-Twilio-Programmable-Messaging
    body = fields.CharField(max_length=320)
    user = fields.ForeignKeyField("models.User", related_name="sent_smss")

    class Meta:
        table = "sent_sms"


class Todo(TimestampMixin, Describable):
    title = fields.CharField(max_length=320)

    # Relationships
    statuses = fields.ManyToManyField(
        "models.TodoStatus",
        through="todo_status_trace",
        related_name="todos",
        forward_key="todo_status_id",
        backward_key="todo_id",
    )

    users: fields.ManyToManyRelation[User]
    todo_status_traces: fields.ReverseRelation["TodoStatusTrace"]

    class Meta:
        table = "todo"

    class PydanticMeta:
        backward_relations = False


class TodoStatus(TimestampMixin, Describable):
    name = fields.CharField(max_length=50, unique=True)
    slug = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "todo_status"


class TodoStatusTrace(TimestampMixin):
    todo = fields.ForeignKeyField("models.Todo")
    todo_status = fields.ForeignKeyField("models.TodoStatus")

    class Meta:
        table = "todo_status_trace"
