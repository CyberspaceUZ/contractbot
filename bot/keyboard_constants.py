from enum import unique, Enum


@unique
class ConvStates(Enum):
    LANGUAGE = 1
    REGISTER = 2


class BotUserReplyKb:
    REGISTER = 'Registration'
    LANGUAGE = 'LANGUAGE'
    CHOICES = (
        (1, LANGUAGE),
        (2, REGISTER),
    )

    @unique
    class CS(Enum):
        REGISTER = 1
