from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app.core.models import TimeStampMixin


class User(AbstractUser):
    pass


class BotUser(TimeStampMixin):
    phone_number = PhoneNumberField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    occupation = models.CharField(max_length=1000, blank=True, null=True)
    chat_id = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'