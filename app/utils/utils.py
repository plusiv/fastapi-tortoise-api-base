# -*- coding: utf-8 -*-
from tortoise import exceptions as db_exception

from app.core.settings import log


def db_exceptions_handler(func):
    log_prefix = "DB_ERROR |"

    error_messages = {
        db_exception.ConfigurationError: "A config error has occurred",
        db_exception.DBConnectionError: "A connection error has occurred",
        db_exception.DoesNotExist: "Data does not exist on database",
        db_exception.FieldError: "There's a problem with a model field",
        db_exception.IncompleteInstanceError: "A partial model has been attempted to be parsed",
        db_exception.IntegrityError: "There's an integrity error on the data",
        db_exception.MultipleObjectsReturned: "Multiple objects returned in .get() operation",
        db_exception.NoValuesFetched: "No values fetched from query",
        db_exception.OperationalError: "An error has occurred in the operation",
        db_exception.ParamsError: "Wrong parameters were given to function",
        db_exception.TransactionManagementError: "A transaction error has occurred",
        db_exception.UnSupportedError: "Operation not supported",
        db_exception.ValidationError: "Could not validate field model",
    }

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except tuple(error_messages.keys()) as e:
            exception_type = type(e).__name__
            error_message = error_messages[type(e)]
            log.error(f"{log_prefix} {error_message} [{exception_type}]: {e}")

    return wrapper
