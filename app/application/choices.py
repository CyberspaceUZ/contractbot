class ApplicationStatus:
    CREATED = 'CREATED'
    IN_PROCESS = 'IN_PROCESS'
    SUCCESS = 'SUCCESS'
    CANCELED = 'CANCELED'

    CHOICES = (
        (CREATED, 'отправлено юристу'),
        (IN_PROCESS, 'на рассмотрении'),
        (SUCCESS, 'согласованно'),
        (CANCELED, 'отказ'),
    )

    CHOICES_DICT = dict(CHOICES)
