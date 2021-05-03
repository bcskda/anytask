import logging
from users.models import UserProfile

logger = logging.getLogger('django.request')
handlers = dict()


def register_handler(command_key):
    def decorator(handler):
        handlers[command_key] = handler
        return handler

    return decorator


@register_handler('start')
def start(update, context):
    reply = 'Visit your profile to get the secret, then call /link <secret>'
    update.message.reply_text(reply)


@register_handler('link')
def link(update, context):
    try:
        secret = context.args[0]
    except Exception:
        update.message.reply_text('Usage: /link <secret>')
        return

    try:
        user_matches = list(UserProfile.objects.filter(telegram_link_secret=secret))
        if len(user_matches) == 0:
            raise KeyError()
    except Exception:
        update.message.reply_text('Invalid secret')
        return

    assert len(user_matches) == 1
    user_profile = user_matches[0]

    tg_uid = update.message.from_user.id
    user_profile.telegram_uid = tg_uid
    user_profile.save()
    # TODO append to user profile log
    # user_profile.user.profiles_users_by_user.objects.add(user_profile)

    update.message.reply_text('Success!')
