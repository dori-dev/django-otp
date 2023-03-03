from random import choices
from django.conf import settings
from django.utils.timezone import now
from kavenegar import (
    KavenegarAPI,
    APIException,
    HTTPException,
)
from background_task import background
from .models import MyUser


@background(schedule=0)
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


def check_otp_expiration(user: MyUser):
    otp_time = user.otp_create_time
    diff = now() - otp_time
    if diff.seconds > 120:
        return False
    return True
