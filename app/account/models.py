from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app.core.models import TimeStampMixin


class User(AbstractUser):
    pass


class BotUser(TimeStampMixin):
    phone_number = PhoneNumberField(null=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=1000, blank=True, null=True)
    chat_id = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.full_name} ({self.chat_id})'

    def has_empty(self):
        return not (self.phone_number and self.full_name and self.company and self.occupation and self.language)

    def update_from_user_data(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    @property
    def msg_detail(self):
        msg = f'User info:\n' \
              f'Name: {self.full_name}\n' \
              f'Company: {self.company}\n' \
              f'Occupation: {self.occupation}\n' \
              f'Phone: {self.phone_number}\n'
        return msg
