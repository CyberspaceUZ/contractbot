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
    APPLICATION = 'Согласовать договор'
    SETTINGS = 'Настройки'

    CHOICE_LIST = (
        APPLICATION,
        SETTINGS,
    )
