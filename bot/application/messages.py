from telegram import Update
from telegram.ext import CallbackContext

from app.territory.models import Territory
from bot.core.constants import BaseChoices
from bot.utils.keyboard import build_reply_kb


def territory_msg(update: Update, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb(Territory.territories_list(), back_btn=True)
    update.message.reply_text(
        'Выберите завод',
        reply_markup=reply_markup
    )


def owner_description_msg(update: Update, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb([BaseChoices.BACK])
    update.message.reply_text(
        'Напишите наименование контрагента и суммы договора',
        reply_markup=reply_markup
    )


def owner_document_msg(update: Update, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb([BaseChoices.BACK])
    update.message.reply_text(
        'Отправьте файл проекта договора',
        reply_markup=reply_markup
    )


def application_create_msg(update: Update, context: CallbackContext, application_id: int, reply_markup=None):
    msg = 'Ваша заявка отправленна юристу\n'
    msg += f'Id: {application_id}'
    update.message.reply_text(
        msg,
        reply_markup=reply_markup
    )


def application_change_msg(chat_id: str, context: CallbackContext, application_id: int, application_status: str,
                           reply_markup=None):
    msg = 'Статус заявки изменен\n'
    msg += f'Id: {application_id}\n' \
           f'Status: {application_status}'
    context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        reply_markup=reply_markup
    )


def receiver_description_msg(chat_id, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb([BaseChoices.BACK])
    msg = 'Напишите замечание'
    context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        reply_markup=reply_markup
    )


def receiver_document_msg(chat_id, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb([BaseChoices.BACK])
    msg = 'Отправьте файл'
    context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        reply_markup=reply_markup
    )


def receiver_description_add_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Замечание прикрепленно',
        reply_markup=reply_markup
    )


def receiver_document_add_msg(update: Update, context: CallbackContext, reply_markup=None):
    update.message.reply_text(
        'Файл прикреплен',
        reply_markup=reply_markup
    )
