from enum import unique, Enum


@unique
class ReportConvStates(Enum):
    REPORT = 0
    LAWYER_REPORT = 1
    OBJECT_REPORT = 2


class ReportChoices:
    LAWYER_REPORT = 'Отчет по моим заявкам'
    OBJECT_REPORT = 'Отчет по заявкам объекта'

    CHOICE_LIST = (
        LAWYER_REPORT,
        OBJECT_REPORT,
    )
