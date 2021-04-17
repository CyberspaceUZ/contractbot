from django.db import models

# Create your models here.
from app.account.models import BotUser
from app.core.models import TimeStampMixin
from app.territory.models import Territory
from app.consultation.choices import ConsultationStatus


class Consultation(TimeStampMixin):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='consultations',
                                  blank=True, null=True)
    owner = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='sent_consultations',
                              blank=True, null=True)
    receiver = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='received_consultations',
                                 blank=True, null=True)
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    status = models.CharField(choices=ConsultationStatus.CHOICES, default=ConsultationStatus.CREATED, max_length=50)
    receiver_msg_id = models.CharField(max_length=128, blank=True, null=True)
    tg_last_kb = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.territory}"
