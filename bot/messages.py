from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from bot.constants import MainMenuChoices
from bot.utils.keyboard import build_reply_kb
from bot.utils.sessionhelper import is_lawyer


def main_menu_msg(update: Update, context: CallbackContext, text=None):
    if not is_lawyer(update.message.chat_id):
        choices = MainMenuChoices.CHOICE_LIST
    else:
        choices = MainMenuChoices.LAWYER_CHOICE_LIST
    update.message.reply_text(
        'Главное меню' if not text else text,
        reply_markup=build_reply_kb(choices, n_cols=1)
    )


def value_add_main_menu_msg(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Добавленно',
        reply_markup=build_reply_kb(MainMenuChoices.CHOICE_LIST, n_cols=1)
    )


def stop_msg(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Нажмите /start',
        reply_markup=ReplyKeyboardMarkup(
            [['/start']],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
