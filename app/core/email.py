# -*- coding: utf-8 -*-
import copy

import aiohttp

from app.core.settings import (
    SENDGRID_API_HEADERS,
    SENDGRID_API_JSON_DATA_TEMPLATE,
    env,
    log,
)
from app.database.models import SentEmail, User


async def send_email(
    subject: str,
    email_to: str,
    template_id: str,
    dynamic_template_data: dict | None = None,
    user_id: str | int | None = None,
):
    """Send email using Sendgrid API.
    This function should be taken as LRO (Long Running Operation).

    Args:
        subject (str): Email subject
        email_to (str): Email to
        template_id (str): Sendgrid template id
        dynamic_template_data (dict, optional): Sendgrid template data. Defaults to None.
        user_id (str | int | None, optional): User id. Defaults to None.

    Returns:
        None
    """
    subject = subject
    to = {"to": [{"email": email_to}]}

    personalizations = dict()
    personalizations.update(to)
    personalizations.update({"dynamic_template_data": dynamic_template_data})

    json_data_copy = copy.deepcopy(SENDGRID_API_JSON_DATA_TEMPLATE)
    json_data_copy.update({"personalizations": [personalizations]})
    json_data_copy.update({"template_id": template_id})

    # Create email data for database
    sent_email: dict[str, str | None] = {
        "email_subject": subject,
        "from_email": env.SENDGRID_SENDER,
        "to_email": email_to,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                str(env.SENDGRID_API_URL),
                headers=SENDGRID_API_HEADERS,
                json=json_data_copy,
            ):
                await SentEmail.create(
                    using_db=None,
                    **sent_email,
                    user=None if not user_id else await User.get(id=user_id),
                )

    except aiohttp.ServerTimeoutError:
        log.error("Request Timeout")
    except aiohttp.TooManyRedirects:
        log.error("Too many redirects")
    except aiohttp.ClientResponseError as e:
        log.error(f"A client response error has occourred {e}")
    except aiohttp.ClientConnectionError as e:
        log.error(f"A client connection error has occourred {e}")
    except aiohttp.ClientError as e:
        log.error(f"A client error has occourred: {e}")

    sent_email.update({"sent_at": None})
    await SentEmail.create(using_db=None, **sent_email)


async def send_wellcome(
    email_to: str,
    first_name: str,
    user_id: int | str,
    template_id: str = env.SENDGRID_NEW_USER_TEMPLATE_ID,
):
    """Send wellcome email to new user.
    This function should be taken as LRO (Long Running Operation).

    Args:
        email_to (str): Email to
        first_name (str): User first name
        user_id (int | str): User id
        template_id (str, optional): Sendgrid template id. Defaults to env.SENDGRID_NEW_USER_TEMPLATE_ID.

    Returns:
        None
    """

    subject = "Verfication Code"

    dynamic_template_data = {
        "first_name": first_name,
        "subject": subject,
    }

    await send_email(
        subject=subject,
        email_to=email_to,
        user_id=user_id,
        template_id=template_id,
        dynamic_template_data=dynamic_template_data,
    )
