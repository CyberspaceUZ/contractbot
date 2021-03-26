from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters


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
