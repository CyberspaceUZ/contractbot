from enum import unique, Enum


@unique
class UserConvStates(Enum):
    LANGUAGE = 0
    PHONE = 1
    FULL_NAME = 2
    COMPANY = 3
    OCCUPATION = 4
    SETTINGS = 5


class LanguageChoices:
    RU = 'RU'
    UZ = 'UZ'

    CHOICE_LIST = (
        RU,
        UZ,
    )

    MESSAGE = 'Выберите язык'


class SettingChoices:
    LANGUAGE = 'Язык'

    CHOICE_LIST = (
        LANGUAGE,
    )
