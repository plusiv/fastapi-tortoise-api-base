# -*- coding: utf-8 -*-
from app.core.settings import log
from tortoise import exceptions as db_exception


def db_exceptions_handler(func):
    log_prefix = "DB_ERROR |"

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except db_exception.ConfigurationError as e:
            log.error(f"{log_prefix} A config error has occurred: {e}")
        except db_exception.DBConnectionError as e:
            log.error(f"{log_prefix} A connection error has occurred: {e}")
        except db_exception.DoesNotExist as e:
            log.error(f"{log_prefix} Data does not exist on databse: {e}")
        except db_exception.FieldError as e:
            log.error(f"{log_prefix} There's a problem with a model field: {e}")
        except db_exception.IncompleteInstanceError as e:
            log.error(
                f"{log_prefix} A partial model has been attempted to be parsed: {e}"
            )
        except db_exception.IntegrityError as e:
            log.error(f"{log_prefix} There's an integrity error on the data: {e}")
        except db_exception.MultipleObjectsReturned as e:
            log.error(
                f"{log_prefix} Multiple objects returned in .get() operation: {e}"
            )
        except db_exception.NoValuesFetched as e:
            log.error(f"{log_prefix} No velues fetched from query: {e}")
        except db_exception.OperationalError as e:
            log.error(f"{log_prefix} An error has occurred in the operation: {e}")
        except db_exception.ParamsError as e:
            log.error(f"{log_prefix} Wrong parameters was given to function: {e}")
        except db_exception.TransactionManagementError as e:
            log.error(f"{log_prefix} A transaction error has occurred: {e}")
        except db_exception.UnSupportedError as e:
            log.error(f"{log_prefix} Operation not supported: {e}")
        except db_exception.ValidationError as e:
            log.error(f"{log_prefix} Could not validate field model: {e}")

    return wrapper
