from enum import Enum, unique


@unique
class ConsultationConvStates(Enum):
    TERRITORY = 0
    QUESTION = 1


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
