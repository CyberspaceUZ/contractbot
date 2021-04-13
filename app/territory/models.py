from django.db import models
from app.core.models import TimeStampMixin


class Territory(TimeStampMixin):
    name = models.CharField(max_length=20, unique=True)
    lawyer = models.ForeignKey('account.BotUser', on_delete=models.SET_NULL, related_name='territories',
                               blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def territories_list():
        return Territory.objects.filter(is_active=True, lawyer__isnull=False) \
            .values_list('name', flat=True).order_by('name')
