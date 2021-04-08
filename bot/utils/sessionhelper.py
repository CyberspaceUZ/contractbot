

def update_user_data(update, context, key, last_choice=None):
    text = update.message.text
    context.user_data[key] = text
    if last_choice:
        context.user_data['last_choice'] = last_choice
    return text, context.user_data


def get_or_none(class_, **kwargs):
    try:
        return class_.objects.get(**kwargs)
    except class_.DoesNotExist:
        pass
    except class_.MultipleObjectsReturned:
        return []
    return None
