# -*- coding: utf-8 -*-
import aiohttp
from app.core.settings import env, log
from app.pydantic_models.message import SentSMSPydantic


async def send_sms(
    number_to: str, body: str = "", number_from: str = env.TWILIO_FROM_NUMBER
) -> SentSMSPydantic:
    data = {
        "Body": body,
        "From": env.TWILIO_FROM_NUMBER,
        "To": number_to,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(env.TWILIO_API_URL, json=data):
                ...

        sent_sms = await SentSMSPydantic.create(
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
    except aiohttp.ClientError as e:
        log.error(f"A client error has occourred: {e}")
    except aiohttp.ClientConnectionError as e:
        log.error(f"A client connection error has occourred {e}")

    sent_sms = await SentSMSPydantic.create(
        from_sms=data.get("FROM"),
        to_sms=data.get("TO"),
        body=data.get("Body"),
        sent_at=None,
    )

    sent_sms_pydantic = await SentSMSPydantic.from_tortoise_orm(sent_sms)
    return sent_sms_pydantic
