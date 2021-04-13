from telegram import Update
from telegram.ext import CallbackContext

from bot.report.constants import ReportChoices
from bot.utils.keyboard import build_reply_kb


def report_msg(update: Update, context: CallbackContext, reply_markup=None):
    if reply_markup is None:
        reply_markup = build_reply_kb(ReportChoices.CHOICE_LIST, n_cols=1, back_btn=True)
    update.message.reply_text(
        'Выберите отчет',
        reply_markup=reply_markup
    )
