from app.account.models import BotUser


class BotUserCallback:
    pass


def bot_user_from_callback(query):
    return BotUser.objects.get(chat_id=query.message.chat_id)
