from django.conf import settings
from telegram import Bot, TelegramError
from telegram.ext import Dispatcher

from mail.base import BaseRenderer, BaseSender

import logging


logger = logging.getLogger('django.request')


class AnyTelegram:
    """Not thread-safe: must be called from single thread"""

    _token = settings.TELEGRAM_TOKEN
    _webhook_url = settings.TELEGRAM_WEBHOOK_URL

    def __init__(self):
        self._bot = None
        self._dispatcher = None

    def get_bot(self):
        if self._bot is None:
            self._bot = Bot(self._token)
        return self._bot

    def get_dispatcher(self):
        if self._dispatcher is None:
            self._dispatcher = Dispatcher(self.get_bot(), update_queue=None, workers=0)
        return self._dispatcher

    def set_webhook(self, **kwargs):
        try:
            return self.get_bot().set_webhook(url=self.get_webhook_url(), **kwargs)
        except TelegramError as e:
            logger.exception('set_webhook', exc_info=e)
            return False

    def delete_webhook(self):
        try:
            return self.get_bot().delete_webhook()
        except TelegramError as e:
            logger.exception('delete_webhook', exc_info=e)
            return False

    @classmethod
    def get_bot_endpoint(cls):
        return 'https://api.telegram.org/bot{}'.format(cls._token)

    @classmethod
    def get_webhook_url(cls):
        return cls._webhook_url


class TelegramRenderer(BaseRenderer):
    def render_notification(self, user_profile, unread_messages):
        return 'Rendered notifications stub'

    def render_fulltext(self, message, recipients):
        return 'Rendered fulltext stub'


class TelegramSender(BaseSender):
    def mass_send(self, prepared_messages):
        logger.info('TelegramSender.mass_send stub:', prepared_messages)
        return 0
