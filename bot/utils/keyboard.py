import json

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Model
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Filters

from bot.core.constants import BaseChoices


class BaseReplyKeyboard:
    objs = []

    def __init__(self, objs, *args, **kwargs):
        super(BaseReplyKeyboard, self).__init__()
        self.objs = objs

    def menu(self, one_time_keyboard=False, resize_keyboard=True, n_cols=2):
        reply_keyboard = build_menu(
            buttons=self.objs,
            n_cols=n_cols,
            # footer_buttons=self.back_btn()
        )
        return ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=one_time_keyboard,
            resize_keyboard=resize_keyboard
        )

    def reg_filters(self):
        reg = f'^({"|".join(self.objs)})$'
        filters = Filters.regex(reg)
        return filters

    # def back_btn(self):
    #     return Choices.BACK

    # def reg_back_filter(self):
    #     reg = f'^{self.back_btn()}$'
    #     filters = Filters.regex(reg)
    #     return filters


def regex_choices_filter(objs):
    reg = f'^({"|".join(objs)})$'
    filters = Filters.regex(reg)
    return filters


def build_reply_kb(objs, one_time_keyboard=True, resize_keyboard=True, n_cols=2, back_btn=False):
    data = dict(
        buttons=objs,
        n_cols=n_cols,
    )
    if back_btn:
        data.update(footer_buttons=BaseChoices.BACK)
    reply_keyboard = build_menu(
        **data
    )
    return ReplyKeyboardMarkup(
        reply_keyboard,
        one_time_keyboard=one_time_keyboard,
        resize_keyboard=resize_keyboard
    )


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def msgs_with_reply_markup_from_qs(qs, actions, msg_template, fields, obj_type=None, n_cols=2):
    objs = list(qs)
    msgs = [
        msg_template.format(
            **{i: getattr(obj, i, None) for i in fields}
        ) for obj in objs
    ]
    if not msgs:
        return None
    objs_buttons = [
        obj_buttons(obj, actions, obj_type=obj_type) for obj in objs
    ]
    menus = [InlineKeyboardMarkup(build_menu(buttons, n_cols)) for buttons in objs_buttons]
    return zip(msgs, menus)


def obj_buttons(obj: Model, actions, obj_type=None):
    """
    :param obj: django Model object
    :param actions: list of list [(action, btn_label, some_field1, some_field2)] some_fileds if optional model fields
    :return: buttons list
    """
    buttons = []
    for act in actions:
        action, label, *fields = act
        if fields:
            label = label.format(*[getattr(obj, field, f'{field} non exists') for field in fields])
        buttons.append(btn_from_obj(obj.id, action, label, obj_type=obj_type))
    return buttons


def btn_from_obj(_id, action, label, obj_type=None):
    data = {'id': _id, 'action': action}
    if obj_type:
        data.update({'type': obj_type})
    return InlineKeyboardButton(
        label,
        callback_data=json.dumps(data)
    )


def btns_to_dict(btns):
    return [[button.to_dict() for button in row] for row in btns]


def dict_to_btns(btns):
    return [[InlineKeyboardButton(**button) for button in row] for row in btns]
