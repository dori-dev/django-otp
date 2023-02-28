from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class MyUser(AbstractUser):
    username = None
    phone = models.CharField(
        max_length=15,
        unique=True,
    )
    otp = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    otp_create_time = models.DateTimeField(
        auto_now=True,
    )
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    backend = ''
