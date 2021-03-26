from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import logging
import subprocess

from telegram import Update

from app.account.models import BotUser
from bot.keyboard_constants import ConvStates
from bot.user_conversation.reply_keyboards import BotUserReplyKeyboard


def start(update: Update, context: CallbackContext) -> ConvStates:
    update.message.reply_text(
        "Hi!",
        reply_markup=BotUserReplyKeyboard.main_menu(),
    )
    BotUser.objects.update_or_create(
        chat_id=update.message.chat_id,
    )
    logging.warning(context.user_data)
    context.user_data.clear()
    # if context.user_data.get('choice'):
    return ConversationHandler.END


def handlers():
    return CommandHandler('start', start)
