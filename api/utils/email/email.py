import copy
import aiohttp

from api import env
from api.database.models import SentEmail
from api.pydantic_models.email import SentEmailPydantic


headers = {
    'Authorization': f'Bearer {env.get("SENDGRID_API_KEY")}',
    'Content-Type': 'application/json',
}

json_data = {
    'from': {
        'email': env.get("SENDGRID_SENDER"),
    },
    'personalizations': [
        {
            'to': [
                {
                    'email': "",
                },
            ],
            'dynamic_template_data': {}
        },
    ],
    'template_id': "",
}

async def send_wellcome(first_name: str,
                  template_id: str = env.get("SENDGRID_NEW_USER_TEMPLATE_ID"),
                  email_to: str = "blackhole@example.com") -> SentEmailPydantic:
    
    subject = f"Welcome {first_name}! Thanks for signing up." 
    to = {"to": [{"email": email_to}]} 
    dynamic_template_data = {
            "dynamic_template_data": {
                "first_name": first_name,
                "subject": subject
                }
            }
    personalizations = dict()
    personalizations.update(to)
    personalizations.update(dynamic_template_data)

    json_data_copy = copy.deepcopy(json_data)
    json_data_copy.update({"personalizations": [personalizations]})
    json_data_copy.update({"template_id": template_id})

    # Create email data for database
    sent_email = {
            "email_subject": subject,
            "from_email": env.get("SENDGRID_SENDER"),
            "to_email": email_to,
            "template_name": "Wellcome 1.0",
            }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(env.get("SENDGRID_API_URL"), headers=headers, json=json_data_copy):
                ...

        sent_email = await SentEmail.create(**sent_email)
        sent_email_pydantic = await SentEmailPydantic.from_tortoise_orm(sent_email)
    
        return sent_email_pydantic

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


    sent_email.update({"sent_at": None})
    sent_email = await SentEmail.create(**sent_email)
    sent_email_pydantic = await SentEmailPydantic.from_tortoise_orm(sent_email)
    
    return sent_email_pydantic


