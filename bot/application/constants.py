from enum import Enum, unique


@unique
class ApplicationConvStates(Enum):
    TERRITORY = 0
    OWNER_DOCUMENT = 1
    OWNER_DESCRIPTION = 2
    APPLICATION = 4


@unique
class ApplicationResultConvStates(Enum):
    APPROVED = 0
    CANCELED = 1
    DESCRIPTION = 2
    DOCUMENT = 3


@unique
class ApplicationActions(Enum):
    START_REVIEW = 0
    USER_INFO = 1
    APPROVED = 2
    CANCELED = 3
    DESCRIPTION = 4
    DOCUMENT = 5
    SEND_CANCELED = 6
    CONTR_AGENT = 7
    AGREEMENT_NUMBER = 8
    DATE_OF_ORIGIN = 9
    MATURITY_DATE = 10
    AMOUNT = 11
    CURRENCY = 12
    TITLE = 13
    COVENANTS = 14
    AGREEMENT = 15
    PERFORMANCE = 16
    PAYMENTS_TERMS = 17
    TRANSFER_RISK = 18
    INCO_TERMS = 19

    LABELS_START = (
        (USER_INFO, 'Информация о заявителе'),
        (START_REVIEW, 'Начать расмотрение'),
    )

    LABELS_RESULT = (
        (USER_INFO, 'Информация о заявителе'),
        (APPROVED, 'Согласованно'),
        (CANCELED, 'Отказ'),
    )

    LABELS_ON_APPROVE = (
        (CONTR_AGENT, 'контрагент'),
        (AGREEMENT_NUMBER, 'номер договора'),
        (DATE_OF_ORIGIN, 'дата заключения договора'),
        (MATURITY_DATE, 'дата истечения срока'),
        (AMOUNT, 'сумма'),
        (CURRENCY, 'валюта'),
        (TITLE, 'предмет договора'),
        (COVENANTS, 'ковенант'),
        (AGREEMENT, 'вид договора'),
        (PERFORMANCE, 'исполнение договора'),
        (PAYMENTS_TERMS, 'условия оплаты'),
        (TRANSFER_RISK, 'переход риска'),
        (INCO_TERMS, 'условия инконермс'),
    )

    LABELS_ON_CANCEL = (
        (USER_INFO, 'Информация о заявителе'),
        (DESCRIPTION, 'Добавить замечание'),
        (DOCUMENT, 'Добавить файл'),
        (SEND_CANCELED, 'Отправить заявителю'),
    )


# class ApplicationResultChoices:
#     APPROVED = 'Согласованно'
#     CANCELED = 'Отказ'
#
#     CHOICES_LIST = (
#         APPROVED,
#         CANCELED,
#     )
