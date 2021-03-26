from telegram import ReplyKeyboardMarkup
from bot.keyboard_constants import BotUserReplyKb


class BotUserReplyKeyboard:

    @staticmethod
    def main_menu():
        reply_keyboard = [
            [BotUserReplyKb.LANGUAGE],
        ]
        return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

