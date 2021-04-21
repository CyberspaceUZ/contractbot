import json

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from app.consultation.choices import ConsultationStatus
from app.consultation.models import Consultation
from bot.consultation.constants import ConsultationActions
from bot.consultation.messages import question_change_msg, receiver_answer_msg
from bot.utils.keyboard import build_menu, obj_buttons, btns_to_dict, dict_to_btns


class ConsultationCallback:

    @staticmethod
    def already_processed():
        return 'Это действие уже было обработанно'

    @staticmethod
    def action_pattern(action: int):
        return rf'^{{"id": \d+, "action": {action}, "type": "consultation"}}$'

    @staticmethod
    def start_review(update: Update, context: CallbackContext):
        query = update.callback_query
        data = json.loads(query.data)
        obj = Consultation.objects.get(id=data['id'])
        if obj.status != ConsultationStatus.CREATED:
            query.answer(ConsultationCallback.already_processed())
            return ConversationHandler.END
        query.answer()
        obj.status = ConsultationStatus.IN_PROCESS
        obj.save()
        question_change_msg(
            obj.owner.chat_id,
            context,
            obj.id,
            ConsultationStatus.CHOICES_DICT[obj.status]
        )
        reply_kb = InlineKeyboardMarkup(
            build_menu(obj_buttons(obj=obj, actions=ConsultationActions.LABELS_RESULT.value, obj_type='consultation'), 1)
        )
        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            text=obj.question,
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
        obj = Consultation.objects.get(id=data['id'])
        context.bot.answer_callback_query(callback_query_id=query.id, text=obj.owner.msg_detail, show_alert=True)
        query.answer()
        return ConversationHandler.END

    @staticmethod
    def answer(update: Update, context: CallbackContext):
        query, data = callback_query_checker_updater(update, context, dict(ConsultationActions.LABELS_RESULT.value))
        context.user_data['f_name'] = 'answer'
        receiver_answer_msg(
            query.message.chat_id,
            context,
        )
        return ConsultationActions.ANSWER


def callback_query_checker_updater(update, context, actions_dict):
    query = update.callback_query
    data = json.loads(query.data)
    query.answer()
    context.user_data['last_choice'] = actions_dict[data['action']]
    context.user_data['app_id'] = data['id']
    btns = btns_to_dict(query.message.reply_markup.inline_keyboard)
    Consultation.objects.filter(id=data['id']).update(tg_last_kb=btns)
    return query, data


def change_application_kb(context, obj, btn_text):
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
