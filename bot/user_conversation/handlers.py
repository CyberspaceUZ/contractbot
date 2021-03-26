from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext, CommandHandler, \
    CallbackQueryHandler
from bot.keyboard_constants import BotUserReplyKb, ConvStates
from bot.handlers import start
from bot.user_conversation.callbacks import BotUserCallback
from bot.utils.keyboard import BaseReplyKeyboard

lang_list = [
    'Uzbek',
    'Russian',
    'English',
]
language_kb = BaseReplyKeyboard(objs=lang_list)


def language(update: Update, context: CallbackContext) -> ConvStates:
    update.message.reply_text(
        'Select Language',
        reply_markup=language_kb.menu(one_time_keyboard=True)
    )
    text = update.message.text
    context.user_data['choice'] = text
    return ConvStates.REGISTER


def user_conv_handler():
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(f'^{BotUserReplyKb.LANGUAGE}$'), language)],
        states={
            # ConvStates.CATEGORY: [
            #     MessageHandler(category_kb.reg_filters(), category),
            #     MessageHandler(category_kb.reg_back_filter(), start)
            # ],
            # ConvStates.DISTRICT: [
            #     MessageHandler(district_kb.reg_filters(), district),
            #     MessageHandler(category_kb.reg_back_filter(), start_service)
            # ],
            # ConvStates.MASTER: [
            #     CallbackQueryHandler(
            #         MasterCallback.like,
            #         pattern=MasterCallback.action_pattern(MasterAction.LIKE.value)
            #     ),
            #     CallbackQueryHandler(
            #         MasterCallback.dislike,
            #         pattern=MasterCallback.action_pattern(MasterAction.DISLIKE.value)
            #     ),
            #     CallbackQueryHandler(
            #         MasterCallback.review,
            #         pattern=MasterCallback.action_pattern(MasterAction.REVIEW.value)
            #     ),
            #     CallbackQueryHandler(
            #         MasterCallback.portfolio,
            #         pattern=MasterCallback.action_pattern(MasterAction.PORTFOLIO.value)
            #     ),
            #     CallbackQueryHandler(
            #         MasterCallback.booking,
            #         pattern=MasterCallback.action_pattern(MasterAction.BOOKING.value)
            #     ),
            #     MessageHandler(master_kb.reg_filters(), master),
            #     MessageHandler(master_kb.reg_back_filter(), category),
            # ],
            # ConvStates.REVIEW: [
            #
            # ]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    return conv_handler
