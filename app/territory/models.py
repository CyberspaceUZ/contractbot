from django.db import models
from app.core.models import TimeStampMixin


# Create your models here.

class Territory(TimeStampMixin):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
