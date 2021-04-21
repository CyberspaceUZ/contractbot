from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from bot.messages import main_menu_msg


def back_to_main(update: Update, context: CallbackContext):
    main_menu_msg(update, context)
    return ConversationHandler.END
