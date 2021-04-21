from django.db import models

from app.account.models import BotUser
from app.application.choices import ApplicationStatus
from app.core.models import TimeStampMixin
from app.territory.models import Territory


class Application(TimeStampMixin):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name='applications',
                                  blank=True, null=True)
    owner = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='sent_applications',
                              blank=True, null=True)
    receiver = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='received_applications',
                                 blank=True, null=True)
    owner_description = models.CharField(max_length=128, blank=True, null=True)
    owner_file = models.FileField(upload_to='documents/owner', blank=True, null=True)
    tg_owner_file_id = models.CharField(max_length=255, blank=True, null=True)
    receiver_description = models.CharField(max_length=128, blank=True, null=True)
    receiver_file = models.FileField(upload_to='documents/receiver', blank=True, null=True)
    tg_receiver_file_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=ApplicationStatus.CHOICES, default=ApplicationStatus.CREATED, max_length=50)
    receiver_msg_id = models.CharField(max_length=128, blank=True, null=True)
    tg_last_kb = models.JSONField(blank=True, null=True)

    contr_agent = models.CharField(max_length=255, blank=True, null=True)
    agreement_number = models.CharField(max_length=255, blank=True, null=True)
    date_of_origin = models.CharField(max_length=255, blank=True, null=True)
    maturity_date = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    covenants = models.CharField(max_length=255, blank=True, null=True)
    agreement = models.CharField(max_length=255, blank=True, null=True)
    performance = models.CharField(max_length=255, blank=True, null=True)
    payment_terms = models.CharField(max_length=255, blank=True, null=True)
    transfer_risk = models.CharField(max_length=255, blank=True, null=True)
    inco_terms = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.territory} {self.owner_description}'

    @property
    def application_detail_msg(self):
        msg = f'{self.owner_description}\n' \
              f'id: {self.id}\n' \
              f'{ApplicationStatus.CHOICES_DICT[self.status]}\n'
        return msg

    @property
    def lawyer_canceled_msg(self):
        msg = f'id: {self.id}\n' \
              f'{ApplicationStatus.CHOICES_DICT[self.status]}\n' \
              f'{self.receiver_description}\n'
        return msg

    @property
    def lawyer_success_msg(self):
        msg = f'id: {self.id}\n' \
              f'{self.status}\n'
        return msg

    @staticmethod
    def report_cols():
        cols = dict(
            id='Id',
            contr_agent='Contragent',
            agreement_number='Agreement number',
            date_of_origin='Date of origin',
            maturity_date='Maturity date',
            amount='Amount',
            currency='Currency',
            title='Title',
            covenants='Existence of financial\n/non-financial covenants',
            agreement='Type of agreement\n(in or out)',
            performance='Performance of a contract',
            payment_terms='Terms of payment',
            transfer_risk='Transfer risk',
            inco_terms='incoterms',
        )
        return cols
