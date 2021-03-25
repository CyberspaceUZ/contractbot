from django.db import models
from app.territory.models import Territory
from app.core.models import TimeStampMixin
from django.contrib.auth.models import AbstractUser
from .choices import UserType
# Create your models here.

class User(AbstractUser, TimeStampMixin):
    phone_number = models.CharField(max_length=13)
    organization_name = models.CharField(max_length=30, null=True, blank=True)
    position = models.CharField(max_length=20, null=True, blank=True)
    type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        if not self.first_name or not self.last_name:
            full_name = self.username
        else:
            full_name = f"{self.last_name} {self.first_name}"
        return full_name