from django.core.files.base import ContentFile
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, CallbackContext, Filters, \
    CallbackQueryHandler

from app.account.models import BotUser
from app.application.models import Application
from app.territory.models import Territory
from bot.application.callbacks import ApplicationCallback, change_application_kb
from bot.application.constants import ApplicationConvStates, ApplicationActions, ApplicationResultConvStates
from bot.application.messages import owner_description_msg, owner_document_msg, territory_msg, application_create_msg
from bot.constants import ConvStates, MainMenuChoices
from bot.core.constants import BaseChoices
from bot.core.handlers import back_to_main
from bot.messages import main_menu_msg, value_add_main_menu_msg
from bot.utils.keyboard import regex_choices_filter, build_menu, obj_buttons, build_reply_kb
from bot.utils.sessionhelper import update_user_data
from app.core.utils.etc import get_or_none

APPLICATION = 'application'
TERRITORY = 'territory'
OWNER_DESCRIPTION = 'owner_description'
OWNER_DOCUMENT = 'owner_document'
RECEIVER_DESCRIPTION = 'receiver_description'


def application(update: Update, context: CallbackContext) -> ApplicationConvStates:
    update_user_data(update, context, APPLICATION, last_choice=APPLICATION)
    territory_msg(update, context)
    return ApplicationConvStates.TERRITORY


def territory(update: Update, context: CallbackContext) -> ApplicationConvStates:
    text, user_data = update_user_data(update, context, TERRITORY, last_choice=TERRITORY)
    obj = get_or_none(Territory, name=text)
    if not obj:
        back_to_main(update, context)
        return ConversationHandler.END
    owner_description_msg(update, context)
    return ApplicationConvStates.OWNER_DESCRIPTION


def owner_description(update: Update, context: CallbackContext) -> ApplicationConvStates:
    update_user_data(update, context, OWNER_DESCRIPTION, last_choice=OWNER_DESCRIPTION)
    owner_document_msg(update, context)
    return ApplicationConvStates.OWNER_DOCUMENT


def owner_document(update: Update, context: CallbackContext) -> ApplicationConvStates:
    obj = Application()
    data = context.user_data.copy()
    ter = Territory.objects.get(name=data.get(TERRITORY))
    obj.territory = ter
    obj.owner = BotUser.objects.get(chat_id=update.message.chat_id)
    obj.receiver = ter.lawyer
    obj.owner_description = data.get(OWNER_DESCRIPTION)
    obj.tg_owner_file_id = update.message.document.file_id
    obj.save()
    file = ContentFile(context.bot.get_file(update.message.document).download_as_bytearray())
    obj.owner_file.save(update.message.document.file_name, file)
    application_create_msg(
        update,
        context,
        obj.id,
        reply_markup=build_reply_kb(MainMenuChoices.CHOICE_LIST, n_cols=1)
    )

    reply_kb = InlineKeyboardMarkup(
        build_menu(
            obj_buttons(obj=obj, actions=ApplicationActions.LABELS_START.value, obj_type='app'),
            1
        )
    )
    receiver_msg = context.bot.send_document(
        chat_id=ter.lawyer.chat_id,
        document=update.message.document.file_id,
        caption=obj.application_detail_msg,
        reply_markup=reply_kb,
    )
    obj.receiver_msg_id = receiver_msg.message_id
    obj.save()
    return ConversationHandler.END


def back(update: Update, context: CallbackContext) -> ApplicationConvStates:
    last_choice = context.user_data.get('last_choice')
    if last_choice == APPLICATION:
        #del context.user_data['last_choice']
        main_menu_msg(update, context)
        return ConversationHandler.END
    elif last_choice == TERRITORY:
        context.user_data['last_choice'] = APPLICATION
        territory_msg(update, context)
        return ApplicationConvStates.TERRITORY
    elif last_choice == OWNER_DESCRIPTION:
        context.user_data['last_choice'] = TERRITORY
        owner_description_msg(update, context)
        return ApplicationConvStates.OWNER_DESCRIPTION

    main_menu_msg(update, context)
    return ConversationHandler.END


def application_handler():
    from bot.handlers import start
    conv_handler = ConversationHandler(
        entry_points=[
            # MessageHandler(regex_choices_filter(Territory.territories_list()), territory),
            MessageHandler(regex_choices_filter([MainMenuChoices.APPLICATION]), application),
        ],
        states={
            ApplicationConvStates.TERRITORY: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back),
                MessageHandler(Filters.text, territory),
            ],
            ApplicationConvStates.OWNER_DESCRIPTION: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back),
                MessageHandler(Filters.text, owner_description),
            ],
            ApplicationConvStates.OWNER_DOCUMENT: [
                MessageHandler(Filters.document, owner_document),
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        map_to_parent={
            ConversationHandler.END: ConvStates.MAIN_MENU,
        },
        name="application_conversation",
        persistent=True,
    )
    return conv_handler


def canceled_description(update: Update, context: CallbackContext) -> ApplicationResultConvStates:
    text = update.message.text
    user_data = context.user_data
    obj = Application.objects.get(id=user_data['app_id'])
    obj.receiver_description = text
    obj.save()
    change_application_kb(
        context,
        obj,
        user_data['last_choice']
    )
    main_menu_msg(update, context, text='Добавленно')
    return ConversationHandler.END


def canceled_document(update: Update, context: CallbackContext) -> ApplicationResultConvStates:
    user_data = context.user_data
    file = ContentFile(context.bot.get_file(update.message.document).download_as_bytearray())
    obj = Application.objects.get(id=context.user_data['app_id'])
    obj.receiver_file.save(update.message.document.file_name, file)
    obj.tg_receiver_file_id = update.message.document.file_id
    obj.save()
    change_application_kb(
        context,
        obj,
        user_data['last_choice']
    )
    main_menu_msg(update, context, text='Добавленно')
    return ConversationHandler.END


def contr_agent(update: Update, context: CallbackContext):
    text = update.message.text
    f_name = context.user_data['f_name']
    obj = Application.objects.get(id=context.user_data['app_id'])
    setattr(obj, f_name, text)
    obj.save()
    change_application_kb(
        context,
        obj,
        context.user_data['last_choice']
    )
    main_menu_msg(update, context, text='Добавленно')
    return ConversationHandler.END


def result_back(update: Update, context: CallbackContext) -> ApplicationResultConvStates:
    main_menu_msg(update, context)
    return ConversationHandler.END


def application_result_handler():
    from bot.handlers import start
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                ApplicationCallback.start_review,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.START_REVIEW.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.user_info,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.USER_INFO.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.approved,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.APPROVED.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.canceled,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.CANCELED.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.canceled_document,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.DOCUMENT.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.canceled_description,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.DESCRIPTION.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.canceled_send,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.SEND_CANCELED.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.contr_agent,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.CONTR_AGENT.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.contr_agent,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.CONTR_AGENT.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.agreement_number,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.AGREEMENT_NUMBER.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.date_of_origin,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.DATE_OF_ORIGIN.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.maturity_date,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.MATURITY_DATE.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.amount,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.AMOUNT.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.currency,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.CURRENCY.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.title,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.TITLE.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.covenants,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.COVENANTS.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.agreement,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.AGREEMENT.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.performance,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.PERFORMANCE.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.payment_terms,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.PAYMENTS_TERMS.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.transfer_risk,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.TRANSFER_RISK.value)
            ),
            CallbackQueryHandler(
                ApplicationCallback.inco_terms,
                pattern=ApplicationCallback.action_pattern(ApplicationActions.INCO_TERMS.value)
            )
        ],
        states={
            ApplicationResultConvStates.DESCRIPTION: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), result_back),
                MessageHandler(Filters.text, canceled_description),
            ],
            ApplicationResultConvStates.DOCUMENT: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), result_back),
                MessageHandler(Filters.document, canceled_document),
            ],
            ApplicationActions.CONTR_AGENT: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), result_back),
                MessageHandler(Filters.text, contr_agent),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True,
        name="application_result_conversation",
        persistent=True,
    )
    return conv_handler
