from mail.base import BaseRenderer, BaseSender

import logging


logger = logging.getLogger('django.request')


def bot_endpoint(token):
    return 'https://api.telegram.org/bot{}'.format(token)


class TelegramRenderer(BaseRenderer):
    def render_notification(self, user_profile, unread_messages):
        return 'Rendered notifications stub'

    def render_fulltext(self, message, recipients):
        return 'Rendered fulltext stub'


class TelegramSender(BaseSender):
    def mass_send(self, prepared_messages):
        logger.info('TelegramSender.mass_send stub:', prepared_messages)
        return 0
