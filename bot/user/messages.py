from telegram import Update
from telegram.ext import CallbackContext

from bot.user.constants import LanguageChoices
from bot.utils.keyboard import build_reply_kb


def language_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        LanguageChoices.MESSAGE,
        reply_markup=build_reply_kb(LanguageChoices.CHOICE_LIST)
    )


def phone_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Напишите номер телефона',
        reply_markup=reply_markup
    )


def full_name_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Напишите Ф.И.О',
        reply_markup=reply_markup
    )


def company_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Напишите наименование ваше компании',
        reply_markup=reply_markup
    )


def occupation_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Напишите вашу должность',
        reply_markup=reply_markup
    )


def settings_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Настройки',
        reply_markup=reply_markup
    )
