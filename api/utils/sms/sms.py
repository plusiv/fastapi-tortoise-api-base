import aiohttp
from api.settings import env
from api.pydantic_models.message import SentSMSPydantic
from api.database.models import SentSMS


async def send_sms(number_to: str, 
                   body: str = "",
                   number_from: str = env.TWILIO_FROM_NUMBER) -> SentSMSPydantic:

    data = {
        'Body': body,
        'From': env.TWILIO_FROM_NUMBER,
        'To': number_to,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(env.TWILIO_API_URL, json=data):
                ...

        sent_sms = await SentSMSP.create(
                from_sms=data.get("FROM"),
                to_sms=data.get("TO"),
                body=data.get("Body"))
        
        sent_sms_pydantic = await SentSMSPydantic.from_tortoise_orm(sent_sms)
        return sent_sms_pydantic
    

    except aiohttp.ServerTimeoutError:
        print("Request Timeout")
    except aiohttp.TooManyRedirects:
        print("Too many redirects")
    except aiohttp.ClientResponseError as e:
        print(f"A client response error has occourred {e}")
    except aiohttp.ClientError as e:
        print(f"A client error has occourred: {e}")
    except aiohttp.ClientConnectionError as e:
        print(f"A client connection error has occourred {e}")

    sent_sms = await SentSMSP.create(
            from_sms=data.get("FROM"),
            to_sms=data.get("TO"),
            body=data.get("Body"),
            sent_at=None)
    
    sent_sms_pydantic = await SentSMSPydantic.from_tortoise_orm(sent_sms)
    return sent_sms_pydantic
