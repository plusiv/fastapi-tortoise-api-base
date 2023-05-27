# This file contains database models that satisfies basic needs. The length
# many of the standards used here has been taken from 
# https://www.geekslop.com/technology-articles/2016/here-are-the-recommended-maximum-data-length-limits-for-common-database-and-programming-fields.
# Some fields like e-mail has been taken from its RFC like the RFC 3696 for 
# e-mail standards.
from tortoise.models import Model
from tortoise import fields
from enum import Enum

class Sex(str, Enum):
    male = "M"
    female = "F"

############### Helper Models ###############
class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True)
    disabled_at = fields.DatetimeField(null=True)


class Describable:
    description = fields.CharField(null=True, max_length=255)

class Message:
    sent_at = fields.DatetimeField(auto_now_add=True, null=True)
    


############### Database Models ###############
class User(Model, TimestampMixin):
    username = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=320, unique=True)
    hashed_password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=70)
    last_name =  fields.CharField(max_length=70)
    sex = fields.CharEnumField(Sex, null=True)
    birthdate = fields.DateField(null=True)
    last_login = fields.DatetimeField(null=True)

    # Relationships
    role = fields.ForeignKeyField('models.Role', related_name='roles')

    class Meta:
        table = "user"

    class PydanticMeta:
        exclude = ["hashed_password"]
    
class Role(Model, TimestampMixin, Describable):
    title = fields.CharField(max_length=50)
    slug = fields.CharField(max_length=50, unique=True)

    # Relationships
    permission = fields.ManyToManyField('models.Permission', related_name='permissions')

    class Meta:
        table = "role"

    class PydanticMeta:
        pass

class Permission(Model, TimestampMixin, Describable):
    title = fields.CharField(max_length=25)
    slug = fields.CharField(max_length=25, unique=True)

    class Meta:
        table = "permission"
    
class SentEmail(Model, Describable, Message):
    email_subject = fields.CharField(max_length=150, null=True)
    from_email = fields.CharField(max_length=320)
    to_email = fields.CharField(max_length=320)
    template_name = fields.CharField(max_length=150, null=True)
    template_id = fields.CharField(max_length=50, null=True)

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
