import json

from telegram.ext import Updater, MessageHandler, Filters

from bot.application.handlers import application_result_handler
from bot.core.constants import BaseChoices
from bot.handlers import handlers as base_handler, stop, start
from bot.utils.keyboard import regex_choices_filter


def test_handler(update, context):
    query = update.callback_query
    data = json.loads(query.data)
    print(data)


def init_dispatcher(updater: Updater):
    dispatcher = updater.dispatcher
    dispatcher.add_handler(base_handler(), 0)
    dispatcher.add_handler(application_result_handler())
    dispatcher.add_handler(MessageHandler(regex_choices_filter([BaseChoices.BACK]), start))
    dispatcher.add_handler(MessageHandler(Filters.regex(f'^Главное меню$'), start))
    dispatcher.add_handler(MessageHandler(Filters.text, stop))
