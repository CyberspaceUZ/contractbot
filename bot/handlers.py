from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from telegram import Update
from app.account.models import BotUser
from bot.application.handlers import application_handler
from bot.constants import ConvStates
from bot.core.constants import BaseChoices
from bot.messages import stop_msg, main_menu_msg
from bot.report.handlers import report_handler
from bot.user.handlers import registration_handler, settings_handler
from bot.user.messages import language_msg
from bot.utils.keyboard import regex_choices_filter


def start(update: Update, context: CallbackContext) -> ConvStates:
    context.user_data.clear()
    user, _ = BotUser.objects.update_or_create(
        chat_id=update.message.chat_id,
        defaults=dict(
            is_active=True
        )
    )
    if user.has_empty():
        language_msg(update, context)
        return ConvStates.REGISTER

    main_menu_msg(update, context)
    # logging.warning(context.user_data)
    # context.user_data.clear()
    return ConvStates.MAIN_MENU


def stop(update: Update, context: CallbackContext) -> int:
    stop_msg(update, context)
    return ConversationHandler.END


def handlers():
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],
        states={
            ConvStates.MAIN_MENU: [
                # MessageHandler(regex_choices_filter([MainMenuChoices.APPLICATION]), application),
                application_handler(),
                settings_handler(),
                report_handler(),
            ],
            ConvStates.REGISTER: [
                registration_handler(),
            ],
            ConvStates.SETTINGS: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), start),

            ],
            ConvStates.APPLICATION: [

            ],
            # ConvStates.CREATE_APPLICATION: [
            #     application_handler(),
            #     MessageHandler(regex_choices_filter([BaseChoices.BACK]), start),
            # ]
        },
        fallbacks=[CommandHandler('stop', stop)],
        allow_reentry=True,
    )
    return conv_handler
