import json

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler

from app.application.choices import ApplicationStatus
from app.application.models import Application
from bot.application.constants import ApplicationActions, ApplicationResultConvStates
from bot.application.messages import application_change_msg, receiver_description_msg, receiver_document_msg
from bot.utils.keyboard import build_menu, obj_buttons, btns_to_dict, dict_to_btns


class ApplicationCallback:

    @staticmethod
    def already_processed():
        return 'Это действие уже было обработанно'

    @staticmethod
    def action_pattern(action: int):
        return rf'^{{"id": \d+, "action": {action}, "type": "app"}}$'

    @staticmethod
    def start_review(update: Update, context: CallbackContext):
        query = update.callback_query
        data = json.loads(query.data)
        obj = Application.objects.get(id=data['id'])
        if obj.status != ApplicationStatus.CREATED:
            query.answer(ApplicationCallback.already_processed())
            return ConversationHandler.END
        query.answer()
        obj.status = ApplicationStatus.IN_PROCESS
        obj.save()
        application_change_msg(
            obj.owner.chat_id,
            context,
            obj.id,
            ApplicationStatus.CHOICES_DICT[obj.status]
        )
        reply_kb = InlineKeyboardMarkup(
            build_menu(obj_buttons(obj=obj, actions=ApplicationActions.LABELS_RESULT.value, obj_type='app'), 1)
        )
        context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            caption=obj.application_detail_msg,
            message_id=obj.receiver_msg_id,
            reply_markup=None
        )
        context.bot.edit_message_reply_markup(
            chat_id=obj.receiver.chat_id,
            message_id=obj.receiver_msg_id,
            reply_markup=reply_kb
        )
        return ConversationHandler.END

    @staticmethod
    def user_info(update: Update, context: CallbackContext):
        query = update.callback_query
        data = json.loads(query.data)
        obj = Application.objects.get(id=data['id'])
        query.answer()
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=obj.owner.msg_detail,
        )
        query.answer()
        return ConversationHandler.END

    @staticmethod
    def canceled(update: Update, context: CallbackContext):
        query = update.callback_query
        data = json.loads(query.data)
        query.answer()
        obj = Application.objects.get(id=data['id'])
        if obj.status != ApplicationStatus.IN_PROCESS:
            query.answer(ApplicationCallback.already_processed())
            return ConversationHandler.END
        obj.status = ApplicationStatus.CANCELED
        reply_kb = InlineKeyboardMarkup(
            build_menu(obj_buttons(obj=obj, actions=ApplicationActions.LABELS_ON_CANCEL.value, obj_type='app'), 1)
        )
        context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            caption=obj.application_detail_msg,
            message_id=obj.receiver_msg_id,
            reply_markup=None
        )
        context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=obj.receiver_msg_id,
            reply_markup=reply_kb
        )
        obj.save()
        return ConversationHandler.END

    @staticmethod
    def canceled_document(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_CANCEL.value))
        # obj = Application.objects.get(id=data['id'])
        # if obj.receiver_file:
        #     query.answer(ApplicationCallback.already_processed())
        #     return ConversationHandler.END
        receiver_document_msg(
            query.message.chat_id,
            context,
        )
        return ApplicationResultConvStates.DOCUMENT

    @staticmethod
    def canceled_description(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_CANCEL.value))
        # obj = Application.objects.get(id=data['id'])
        # if obj.receiver_description:
        #     query.answer(ApplicationCallback.already_processed())
        #     return ConversationHandler.END
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        return ApplicationResultConvStates.DESCRIPTION

    @staticmethod
    def canceled_send(update: Update, context: CallbackContext):
        query = update.callback_query
        data = json.loads(query.data)
        obj = Application.objects.get(id=data['id'])
        if not obj.receiver_description or not obj.receiver_file:
            query.answer('Необходимо добавить файл и замечание')
            return ConversationHandler.END
        query.answer()
        context.bot.send_document(
            chat_id=obj.owner.chat_id,
            document=obj.tg_receiver_file_id,
            caption=obj.lawyer_canceled_msg
        )
        context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            caption=obj.application_detail_msg,
            message_id=obj.receiver_msg_id,
            reply_markup=None
        )
        return ConversationHandler.END

    @staticmethod
    def approved(update: Update, context: CallbackContext):
        query = update.callback_query
        data = json.loads(query.data)
        query.answer()
        obj = Application.objects.get(id=data['id'])
        obj.status = ApplicationStatus.SUCCESS
        obj.save()
        application_change_msg(
            obj.owner.chat_id,
            context,
            obj.id,
            ApplicationStatus.CHOICES_DICT[obj.status]
        )
        context.bot.edit_message_caption(
            chat_id=query.message.chat_id,
            caption=obj.application_detail_msg,
            message_id=obj.receiver_msg_id,
            reply_markup=None
        )
        reply_kb = InlineKeyboardMarkup(
            build_menu(obj_buttons(obj=obj, actions=ApplicationActions.LABELS_ON_APPROVE.value, obj_type='app'), 1)
        )
        context.bot.edit_message_reply_markup(
            chat_id=query.message.chat_id,
            message_id=obj.receiver_msg_id,
            reply_markup=reply_kb
        )
        return ConversationHandler.END

    @staticmethod
    def contr_agent(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'contr_agent'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def agreement_number(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'agreement_number'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.AGREEMENT_NUMBER
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def date_of_origin(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'date_of_origin'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.DATE_OF_ORIGIN
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def maturity_date(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'maturity_date'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.MATURITY_DATE
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def amount(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'amount'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.AMOUNT
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def currency(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'currency'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.CURRENCY
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def title(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'title'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.TITLE
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def covenants(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'covenants'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.COVENANTS
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def agreement(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'agreement'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.AGREEMENT
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def performance(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'performance'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.PERFORMANCE
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def payment_terms(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'payment_terms'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.PAYMENTS_TERMS
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def transfer_risk(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'transfer_risk'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.TRANSFER_RISK
        return ApplicationActions.CONTR_AGENT

    @staticmethod
    def inco_terms(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ApplicationActions.LABELS_ON_APPROVE.value))
        context.user_data['f_name'] = 'inco_terms'
        receiver_description_msg(
            query.message.chat_id,
            context,
        )
        # return ApplicationActions.INCO_TERMS
        return ApplicationActions.CONTR_AGENT


def callback_query_checker_updater(update, context, actions_dict):
    query = update.callback_query
    data = json.loads(query.data)
    query.answer()
    context.user_data['last_choice'] = actions_dict[data['action']]
    context.user_data['app_id'] = data['id']
    # btns = [[button.to_dict() for button in row] for row in query.message.reply_markup.inline_keyboard]
    btns = btns_to_dict(query.message.reply_markup.inline_keyboard)
    Application.objects.filter(id=data['id']).update(tg_last_kb=btns)
    return query, data


def change_application_kb(context, obj, btn_text):
    # btns = build_menu(obj_buttons(obj=obj, actions=actions, obj_type='app'), 1)
    # btns = obj.tg_last_kb
    # btns = [[InlineKeyboardButton(**button) for button in row] for row in obj.tg_last_kb]
    btns = dict_to_btns(obj.tg_last_kb)
    for item in btns:
        if item[0].text == btn_text:
            item[0].text = btn_text + ' ☑️'
            context.bot.edit_message_reply_markup(
                chat_id=obj.receiver.chat_id,
                message_id=obj.receiver_msg_id,
                reply_markup=InlineKeyboardMarkup(btns)
            )
            obj.tg_last_kb = btns_to_dict(btns)
            obj.save()
