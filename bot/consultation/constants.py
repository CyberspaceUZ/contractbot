from enum import Enum, unique


@unique
class ConsultationConvStates(Enum):
    TERRITORY = 0
    QUESTION = 1


@unique
class ApplicationResultConvStates(Enum):
    APPROVED = 0
    CANCELED = 1
    DESCRIPTION = 2
    DOCUMENT = 3


@unique
class ConsultationActions(Enum):
    START_REVIEW = 0
    USER_INFO = 1
    ANSWER = 2

    LABELS_START = (
        (USER_INFO, 'Информация о заявителе'),
        (START_REVIEW, 'Начать расмотрение'),
    )

    LABELS_RESULT = (
        (USER_INFO, 'Информация о заявителе'),
        (ANSWER, 'Отвечать'),
    )

# class ApplicationResultChoices:
#     APPROVED = 'Согласованно'
#     CANCELED = 'Отказ'
#
#     CHOICES_LIST = (
#         APPROVED,
#         CANCELED,
#     )
