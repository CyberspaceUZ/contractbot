from django.db import models
from app.core.models import TimeStampMixin
from app.account.models import User
# Create your models here.

class Application(TimeStampMixin):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications_received')
    file = models.FileField(upload_to='files/', )
    note = models.CharField(max_length=100, null=True, blank=True)
