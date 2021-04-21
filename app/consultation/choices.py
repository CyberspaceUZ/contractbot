class ConsultationStatus:
    CREATED = 'CREATED'
    IN_PROCESS = 'IN_PROCESS'
    SUCCESS = 'SUCCESS'

    CHOICES = (
        (CREATED, 'отправлено юристу'),
        (IN_PROCESS, 'на рассмотрении'),
        (SUCCESS, 'ответил'),
    )

    CHOICES_DICT = dict(CHOICES)
