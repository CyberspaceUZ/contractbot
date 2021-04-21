import logging

from app.account.models import BotUser


def update_user_data(update, context, key, last_choice=None):
    if update.message.contact:
        text = update.message.contact.phone_number
    else:
        text = update.message.text
    context.user_data[key] = text
    if last_choice:
        context.user_data['last_choice'] = last_choice
    return text, context.user_data


def is_lawyer(chat_id, return_user=False):
    user = BotUser.objects.get(chat_id=chat_id)
    if return_user:
        return user.territories.exists(), user
    return user.territories.exists()
