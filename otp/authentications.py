from django.shortcuts import redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from .models import MyUser
from . import utils


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user: MyUser = MyUser.objects.get(phone=username)
            if not utils.check_otp_expiration(user):
                messages.error(
                    request,
                    'Your verification code is expired!',
                    extra_tags='danger',
                )
                return None
            if not password.isdigit() or user.otp != int(password):
                messages.error(
                    request,
                    'Wrong verification code entered.',
                    extra_tags='danger',
                )
                return None
        except MyUser.DoesNotExist:
            messages.error(
                request,
                'First send request to send verification code.',
                extra_tags='danger',
            )
            return None
        return user
