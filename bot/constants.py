from enum import unique, Enum


@unique
class ConvStates(Enum):
    START = 0
    MAIN_MENU = 1
    REGISTER = 2
    SETTINGS = 3
    APPLICATION = 4
    CREATE_APPLICATION = 5


class MainMenuChoices:
    APPLICATION = "Согласовать договор"
    CONSULTATION = "Юридическая консультация"
    REPORT = "Отчеты"
    SETTINGS = "Настройки"

    CHOICE_LIST = (
        APPLICATION,
        CONSULTATION,
        SETTINGS,
    )

    LAWYER_CHOICE_LIST = (
        APPLICATION,
        CONSULTATION,
        REPORT,
        SETTINGS,
    )
