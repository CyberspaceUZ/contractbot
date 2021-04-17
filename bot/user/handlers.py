from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext, CommandHandler

from app.account.models import BotUser
from bot.constants import ConvStates, MainMenuChoices
from bot.core.constants import BaseChoices
from bot.core.handlers import back_to_main
from bot.messages import main_menu_msg
from bot.user.constants import LanguageChoices, UserConvStates, SettingChoices
from bot.user.messages import phone_msg, full_name_msg, company_msg, occupation_msg, language_msg, settings_msg
from bot.utils.keyboard import regex_choices_filter, build_reply_kb
from bot.utils.sessionhelper import update_user_data


def language(update: Update, context: CallbackContext) -> UserConvStates:
    update_user_data(update, context, 'language')
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton('Поделиться контактом', request_contact=True)]], resize_keyboard=True)
    phone_msg(update, context, reply_markup=reply_markup)
    return UserConvStates.PHONE


def phone_number(update: Update, context: CallbackContext) -> UserConvStates:
    update_user_data(update, context, 'phone_number')
    reply_markup = ReplyKeyboardRemove()
    full_name_msg(update, context, reply_markup=reply_markup)
    return UserConvStates.FULL_NAME


def full_name(update: Update, context: CallbackContext) -> UserConvStates:
    update_user_data(update, context, 'full_name')
    company_msg(update, context)
    return UserConvStates.COMPANY


def company(update: Update, context: CallbackContext) -> UserConvStates:
    update_user_data(update, context, 'company')
    occupation_msg(update, context)
    return UserConvStates.OCCUPATION


def occupation(update: Update, context: CallbackContext) -> UserConvStates:
    text, user_data = update_user_data(update, context, 'occupation')
    BotUser.objects.get(chat_id=update.message.chat_id).update_from_user_data(**user_data)
    context.user_data.clear()
    main_menu_msg(update, context)
    return ConversationHandler.END


def registration_handler():
    from bot.handlers import start
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(regex_choices_filter(LanguageChoices.CHOICE_LIST), language),
        ],
        states={
            UserConvStates.PHONE: [
                MessageHandler(Filters.text | Filters.contact, phone_number),
            ],
            UserConvStates.FULL_NAME: [
                MessageHandler(Filters.text, full_name),
            ],
            UserConvStates.COMPANY: [
                MessageHandler(Filters.text, company),
            ],
            UserConvStates.OCCUPATION: [
                MessageHandler(Filters.text, occupation),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        map_to_parent={
            ConvStates.REGISTER: ConvStates.REGISTER,
            ConvStates.SETTINGS: ConvStates.SETTINGS,
            ConversationHandler.END: ConvStates.MAIN_MENU,
        },
        name="registration_conversation",
        persistent=True,
    )
    return conv_handler


def user_settings(update: Update, context: CallbackContext) -> UserConvStates:
    settings_msg(update, context, reply_markup=build_reply_kb(SettingChoices.CHOICE_LIST, back_btn=True))
    return UserConvStates.SETTINGS


def settings_language(update: Update, context: CallbackContext) -> UserConvStates:
    last_choice = context.user_data.get('last_choice')
    if last_choice:
        BotUser.objects.filter(chat_id=update.message.chat_id).update(language=update.message.text)
        del context.user_data['language']
        settings_msg(update, context, reply_markup=build_reply_kb(SettingChoices.CHOICE_LIST, back_btn=True))
        return UserConvStates.SETTINGS
    update_user_data(update, context, 'language', last_choice='language')
    language_msg(update, context)
    return UserConvStates.LANGUAGE


def back(update: Update, context: CallbackContext) -> UserConvStates:
    context.user_data.clear()
    settings_msg(update, context, reply_markup=build_reply_kb(SettingChoices.CHOICE_LIST, back_btn=True))
    return UserConvStates.SETTINGS


def settings_handler():
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(regex_choices_filter([MainMenuChoices.SETTINGS]), user_settings),
        ],
        states={
            UserConvStates.LANGUAGE: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back),
                MessageHandler(regex_choices_filter(LanguageChoices.CHOICE_LIST), settings_language),
            ],
            UserConvStates.SETTINGS: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back_to_main),
                MessageHandler(regex_choices_filter([SettingChoices.LANGUAGE]), settings_language),
            ]
        },
        fallbacks=[CommandHandler('stop', back_to_main)],
        map_to_parent={
            ConversationHandler.END: ConvStates.MAIN_MENU,
        },
        allow_reentry=True,
        name="settings_conversation",
        persistent=True,
    )
    return conv_handler
