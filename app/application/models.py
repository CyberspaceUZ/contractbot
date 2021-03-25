from django.db import models

from app.account.models import BotUser
from app.application.choices import ApplicationStatus
from app.core.models import TimeStampMixin
from app.territory.models import Territory


class Application(TimeStampMixin):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='applications')
    owner = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='sent_applications')
    receiver = models.ForeignKey(BotUser, on_delete=models.CASCADE, null=True, related_name='received_applications')
    owner_description = models.CharField(max_length=128, blank=True, null=True)
    owner_file = models.FileField()
    receiver_description = models.CharField(max_length=128, blank=True, null=True)
    receiver_file = models.FileField()
    status = models.CharField(choices=ApplicationStatus.CHOICES, default=ApplicationStatus.CREATED, max_length=50)

    def __str__(self):
        return f'{self.territory} {self.owner_description}'
