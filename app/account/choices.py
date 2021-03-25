from django.db import models

class UserType(models.Model):
    COUNTERPARY = 1
    LAWYER = 2
    USER_TYPE_CHOICES = (
        (COUNTERPARY, 'counterparty'),
        (LAWYER, 'lawyer')
    )

    id = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()
