from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, CallbackContext, Filters, \
    CallbackQueryHandler

from app.account.models import BotUser
from app.consultation.models import Consultation
from app.consultation.choices import ConsultationStatus
from app.territory.models import Territory
from bot.constants import ConvStates, MainMenuChoices
from bot.core.constants import BaseChoices
from bot.core.handlers import back_to_main
from bot.messages import main_menu_msg
from bot.utils.keyboard import regex_choices_filter, build_menu, obj_buttons, build_reply_kb
from bot.utils.sessionhelper import update_user_data
from app.core.utils.etc import get_or_none

from bot.consultation.constants import ConsultationConvStates, ConsultationActions
from bot.consultation.messages import question_msg, question_create_msg
from bot.consultation.callbacks import ConsultationCallback, change_application_kb
from bot.application.messages import territory_msg

CONSULTATION = 'consultation'
TERRITORY = 'territory'
QUESTION = 'question'


def consultation(update: Update, context: CallbackContext) -> ConsultationConvStates:
    update_user_data(update, context, CONSULTATION, last_choice=CONSULTATION)
    territory_msg(update, context)
    return ConsultationConvStates.TERRITORY


def territory(update: Update, context: CallbackContext) -> ConsultationConvStates:
    text, user_data = update_user_data(update, context, TERRITORY, last_choice=TERRITORY)
    obj = get_or_none(Territory, name=text)
    if not obj:
        back_to_main(update, context)
        return ConversationHandler.END
    question_msg(update, context)
    return ConsultationConvStates.QUESTION


def question(update: Update, context: CallbackContext):
    obj = Consultation()
    data = context.user_data.copy()
    ter = Territory.objects.get(name=data.get(TERRITORY))
    obj.territory = ter
    obj.receiver = ter.lawyer
    obj.owner = BotUser.objects.get(chat_id=update.message.chat_id)
    obj.question = update.message.text
    obj.save()
    question_create_msg(
        update,
        context,
        obj.id,
        reply_markup=build_reply_kb(MainMenuChoices.CHOICE_LIST, n_cols=1)
    )
    reply_kb = InlineKeyboardMarkup(
        build_menu(
            obj_buttons(obj=obj, actions=ConsultationActions.LABELS_START.value, obj_type='consultation'),
            1
        )
    )
    receiver_msg = context.bot.send_message(
        chat_id=ter.lawyer.chat_id,
        text=update.message.text,
        reply_markup=reply_kb,
    )
    obj.receiver_msg_id = receiver_msg.message_id
    obj.save()
    return ConversationHandler.END


def back(update: Update, context: CallbackContext) -> ConsultationConvStates:
    last_choice = context.user_data.get('last_choice')
    if last_choice == CONSULTATION:
        del context.user_data['last_choice']
        main_menu_msg(update, context)
        return ConversationHandler.END
    elif last_choice == TERRITORY:
        context.user_data['last_choice'] = CONSULTATION
        territory_msg(update, context)
        return ConsultationConvStates.TERRITORY
    elif last_choice == QUESTION:
        context.user_data['last_choice'] = TERRITORY
        question_msg(update, context)
        return ConsultationConvStates.QUESTION

    main_menu_msg(update, context)
    return ConversationHandler.END


def consultation_handler():
    from bot.handlers import start
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(regex_choices_filter([MainMenuChoices.CONSULTATION]), consultation),
        ],
        states={
            ConsultationConvStates.TERRITORY: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back),
                MessageHandler(Filters.text, territory),
            ],
            ConsultationConvStates.QUESTION: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), back),
                MessageHandler(Filters.text, question),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        map_to_parent={
            ConversationHandler.END: ConvStates.MAIN_MENU,
        },
        name="consultation_conversation",
        persistent=True,
    )
    return conv_handler


def answer(update: Update, context: CallbackContext):
    text = update.message.text
    f_name = context.user_data['f_name']
    obj = Consultation.objects.get(id=context.user_data['app_id'])
    setattr(obj, f_name, text)
    obj.status = ConsultationStatus.SUCCESS
    obj.save()
    change_application_kb(
        context,
        obj,
        context.user_data['last_choice']
    )
    context.bot.send_message(
        chat_id=obj.owner.chat_id,
        text=f"Ответ на ваш {obj.id} вопрос\n{text}",
    )
    main_menu_msg(update, context, text='Добавленно')
    return ConversationHandler.END


def result_back(update: Update, context: CallbackContext):
    context.user_data.clear()
    main_menu_msg(update, context)
    return ConversationHandler.END


def consultation_answer_handler():
    from bot.handlers import start
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                ConsultationCallback.start_review,
                pattern=ConsultationCallback.action_pattern(ConsultationActions.START_REVIEW.value)
            ),
            CallbackQueryHandler(
                ConsultationCallback.user_info,
                pattern=ConsultationCallback.action_pattern(ConsultationActions.USER_INFO.value)
            ),
            CallbackQueryHandler(
                ConsultationCallback.answer,
                pattern=ConsultationCallback.action_pattern(ConsultationActions.ANSWER.value)
            ),
        ],
        states={
            ConsultationActions.ANSWER: [
                MessageHandler(regex_choices_filter([BaseChoices.BACK]), result_back),
                MessageHandler(Filters.text, answer),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True,
        name="consultation_answer_conversation",
        persistent=True,
    )
    return conv_handler
