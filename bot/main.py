from telegram.ext import Updater
from bot.handlers import handlers as base_handler
from bot.user_conversation.handlers import user_conv_handler


def init_dispatcher(updater: Updater):
    dispatcher = updater.dispatcher
    dispatcher.add_handler(base_handler())
    dispatcher.add_handler(user_conv_handler())
