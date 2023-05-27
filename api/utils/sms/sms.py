import os
import requests


async def send_sms(number_to: str, 
                   number_from: str = env.get(TWILIO_FROM_NUMBER),
                   body: str) -> SentSMS:

    data = {
        'Body': body,
        'From': env.get(TWILIO_FROM_NUMBER),
        'To': number_to,
    }

    try:
        response = requests.post(
            env.get('TWILIO_API_URL'),
            data=data,
            auth=(env.get('TWILIO_ACCOUNT_SID'), env.get('TWILIO_AUTH_TOKEN'))
        )
