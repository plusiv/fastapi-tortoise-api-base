# This file contains database models that satisfies basic needs. The length
# many of the standards used here has been taken from 
# https://www.geekslop.com/technology-articles/2016/here-are-the-recommended-maximum-data-length-limits-for-common-database-and-programming-fields.
# Some fields like e-mail has been taken from its RFC like the RFC 3696 for 
# e-mail standards.
from tortoise.models import Model
from tortoise import fields


############### Helper Models ###############
class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True)
    disabled_at = fields.DatetimeField(null=True)


class Describable:
    description = fields.CharField(null=True, max_length=255)


############### Database Models ###############
class User(Model, TimestampMixin):
    username = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=320, unique=True)
    hashed_password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=70)
    last_name =  fields.CharField(max_length=70)
    sex = fields.BooleanField()
    birthday = fields.DateField(null=True)
    last_login = fields.DatetimeField(null=True)

    # Relationships
    role = fields.ForeignKeyField('models.Role', related_name='roles')

    class PydanticMeta:
        exclude = ["hashed_password"]
    
class Role(Model, TimestampMixin, Describable):
    title = fields.CharField(max_length=50)
    slug = fields.CharField(max_length=50, unique=True)

    # Relationships
    permission = fields.ManyToManyField('models.Permission', related_name='permissions')

    class PydanticMeta:
        pass

class Permission(Model, TimestampMixin, Describable):
    title = fields.CharField(max_length=25)
    slug = fields.CharField(max_length=25, unique=True)
    
class SentEmail(Model, Describable):
    email_subject = fields.CharField(max_length=150, null=True)
    from_email = fields.CharField(max_length=320)
    to_email = fields.CharField(max_length=320)
    template_name = fields.CharField(max_length=150, null=True)
    template_id = fields.CharField(max_length=50, null=True)
    sent_at = fields.DatetimeField(auto_now_add=True, null=True)

    class Meta:
        table = "sent_email"

    class PydanticMeta:
        exclude = ["template_id"]
