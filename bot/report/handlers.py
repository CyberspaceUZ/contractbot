from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, CallbackContext, CommandHandler

from app.application.choices import ApplicationStatus
from app.application.models import Application
from app.core.utils.etc import export_to_excel
from app.territory.models import Territory
from bot.constants import MainMenuChoices, ConvStates
from bot.core.constants import BaseChoices
from bot.core.handlers import back_to_main
from bot.report.constants import ReportConvStates, ReportChoices
from bot.report.messages import report_msg
from bot.utils.keyboard import regex_choices_filter
import pandas as pd

from bot.utils.sessionhelper import is_lawyer


def report(update: Update, context: CallbackContext) -> ReportConvStates:
    report_msg(update, context)
    return ReportConvStates.REPORT


def lawyer_report(update: Update, context: CallbackContext) -> ReportConvStates:
    lawyer, user = is_lawyer(update.message.chat_id, return_user=True)
    if not lawyer:
        return ConversationHandler.END
    cols = Application.report_cols()
    qs = Application.objects.filter(status=ApplicationStatus.SUCCESS, receiver=user).values(*cols.keys())
    df = pd.DataFrame(qs)
    df.rename(columns=cols, inplace=True)
    document = export_to_excel(df)
    document.name = f'Отчет по миом заявкам {user.full_name}.xlsx'
    context.bot.send_document(
        chat_id=update.message.chat_id,
        document=document
    )
    return ReportConvStates.REPORT


def object_report(update: Update, context: CallbackContext) -> ReportConvStates:
    lawyer, user = is_lawyer(update.message.chat_id, return_user=True)
    if not lawyer:
        return ConversationHandler.END
    territory = Territory.objects.filter(lawyer=lawyer).first()
    cols = Application.report_cols()
    qs = Application.objects.filter(status=ApplicationStatus.SUCCESS, territory=territory).values(*cols.keys())
    df = pd.DataFrame(qs)
    df.rename(columns=cols, inplace=True)
    document = export_to_excel(df)
    document.name = f'Отчет по объекту {territory.name}.xlsx'
    context.bot.send_document(
        chat_id=update.message.chat_id,
        document=document
    )
    return ReportConvStates.REPORT


def report_handler():
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(regex_choices_filter([MainMenuChoices.REPORT]), report),
        ],
        states={
            ReportConvStates.REPORT: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back_to_main),
                MessageHandler(regex_choices_filter([ReportChoices.LAWYER_REPORT]), lawyer_report),
                MessageHandler(regex_choices_filter([ReportChoices.OBJECT_REPORT]), object_report),
            ]
        },
        fallbacks=[CommandHandler('stop', back_to_main)],
        map_to_parent={
            ConversationHandler.END: ConvStates.MAIN_MENU,
        },
        allow_reentry=True,
        name="report_conversation",
        persistent=True,
    )
    return conv_handler
