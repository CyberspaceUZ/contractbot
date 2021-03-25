class ApplicationStatus:
    CREATED = 'CREATED'
    IN_PROCESS = 'IN_PROCESS'
    SUCCESS = 'SUCCESS'
    CANCELED = 'CANCELED'
    CHOICES = (
        (CREATED, 'Application Created'),
        (IN_PROCESS, 'Application In Process'),
        (SUCCESS, 'Application Succeed'),
        (CANCELED, 'Application Canceled'),
    )
