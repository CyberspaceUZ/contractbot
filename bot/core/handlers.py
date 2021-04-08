from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from bot.messages import main_menu_msg


def back_to_main(update: Update, context: CallbackContext):
    context.user_data.clear()
    main_menu_msg(update, context)
    return ConversationHandler.END
