from enum import unique, Enum
from django.utils.translation import gettext_lazy as _

@unique
class ConvStates(Enum):
    START = 0
    MAIN_MENU = 1
    REGISTER = 2
    SETTINGS = 3
    APPLICATION = 4
    CREATE_APPLICATION = 5


class MainMenuChoices:
    APPLICATION = str(_("Согласовать договор"))
    CONSULTATION = str(_("Юридическая консультация"))
    REPORT = str(_("Отчеты"))
    SETTINGS = str(_("Настройки"))

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
