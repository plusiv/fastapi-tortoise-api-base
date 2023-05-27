import os
import aiohttp


async def send_sms(number_to: str, 
                   number_from: str = env.get(TWILIO_FROM_NUMBER),
                   body: str) -> SentSMS:

    data = {
        'Body': body,
        'From': env.get(TWILIO_FROM_NUMBER),
        'To': number_to,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(env.get("TWILIO_API_URL"), json=data):
                ...
    

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

