from random import choices
from django.conf import settings
from kavenegar import (
    KavenegarAPI,
    APIException,
    HTTPException,
)


def send_otp(phone, otp):
    try:
        api = KavenegarAPI(settings.API_KEY)
        params = {
            'receptor': phone,
            'template': 'verify',
            'token': otp,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
    except APIException:
        response = None
    except HTTPException:
        response = None
    return response


def generate_otp(length=4):
    return "".join(choices("123456789", k=length))