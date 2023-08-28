# -*- coding: utf-8 -*-
import aiohttp
from tortoise.contrib.pydantic.base import PydanticModel

from app.core.settings import env, log
from app.database.models import SentSMS
from app.pydantic_models.messages import SentSMSPydantic


async def send_sms(
    number_to: str, body: str = "", number_from: str = env.TWILIO_FROM_NUMBER
) -> PydanticModel:
    data = {
        "Body": body,
        "From": number_from,
        "To": number_to,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(str(env.TWILIO_API_URL), json=data):
                ...

        sent_sms = await SentSMS.create(
            from_sms=data.get("FROM"), to_sms=data.get("TO"), body=data.get("Body")
        )

        sent_sms_pydantic = await SentSMSPydantic.from_tortoise_orm(sent_sms)
        return sent_sms_pydantic

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

    sent_sms = await SentSMS.create(
        from_sms=data.get("FROM"),
        to_sms=data.get("TO"),
        body=data.get("Body"),
        sent_at=None,
    )

    sent_sms_pydantic = await SentSMSPydantic.from_tortoise_orm(sent_sms)
    return sent_sms_pydantic
