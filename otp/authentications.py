from django.contrib.auth.backends import ModelBackend
from .models import MyUser


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(phone=username)
        except MyUser.DoesNotExist:
            user = None
        return user
