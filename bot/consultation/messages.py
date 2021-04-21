from telegram import Update
from telegram.ext import CallbackContext

from django.utils.translation import activate, gettext_lazy as _

from bot.core.constants import BaseChoices
from bot.utils.keyboard import build_reply_kb


def question_msg(update: Update, context: CallbackContext, reply_markup=None):
    activate(context.user_data.get("language").lower())
    if reply_markup is None:
        reply_markup = build_reply_kb([BaseChoices().get_back()])

    update.message.reply_text(
        str(_('Напишите свой вопрос')),
        reply_markup=reply_markup
    )


def question_create_msg(update: Update, context: CallbackContext, consultation_id: int, reply_markup=None):
    msg = 'Ваша вопрос отправленна юристу\n'
    msg += f'Id: {consultation_id}'
    update.message.reply_text(
        msg,
        reply_markup=reply_markup
    )


def question_change_msg(chat_id: str, context: CallbackContext, consultation_id: int, consultation_status: str, reply_markup=None):
    msg = 'Статус вопрос изменен\n'
    msg += f'Id: {consultation_id}\n' \
           f'Status: {consultation_status}'
    context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        reply_markup=reply_markup
    )


def receiver_answer_msg(chat_id, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb([BaseChoices.BACK])
    msg = 'Напишите ответ'
    context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        reply_markup=reply_markup
    )
