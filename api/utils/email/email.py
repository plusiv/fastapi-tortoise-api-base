import copy
import requests

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
        response = requests.post(env.get("SENDGRID_API_URL"), headers=headers, json=json_data_copy)
        response.raise_for_status()
        sent_email = await SentEmail.create(**sent_email)
        sent_email_pydantic = await SentEmailPydantic.from_tortoise_orm(sent_email)
    
        return sent_email_pydantic

    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Request Timeout")
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Too many redirects")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(f"An exception has accourred: {e}")


    sent_email.update({"sent_at": None})
    sent_email = await SentEmail.create(**sent_email)
    sent_email_pydantic = await SentEmailPydantic.from_tortoise_orm(sent_email)
    
    return sent_email_pydantic


