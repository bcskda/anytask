from django.conf import settings
from django.template.loader import render_to_string

from telegram import Bot, Update, TelegramError
from telegram.ext import Dispatcher, CommandHandler

from bot_handlers import handlers

from mail.base import BaseRenderer, BaseSender
from mail.common import enable_translation

import json
import logging


logger = logging.getLogger('django.request')


class AnyTelegram:
    """Not thread-safe: must be called from single thread"""

    _token = settings.TELEGRAM_TOKEN or '1234567890:ABCDEFGHIJKLMONPQRSTUVWXYZ1234567-8'
    _webhook_url = settings.TELEGRAM_WEBHOOK_URL or ''

    def __init__(self, base_url=None):
        """
        Args:
            base_url: as in telegram.Bot.__init__()
        """
        self._base_url = base_url
        self._bot = None
        self._dispatcher = None

    def _error_handler(self, update, context):
        logger.exception('Unhandled exception %s processing %s',
                         context.error, update,
                         exc_info=context.error)

    def get_bot(self):
        if self._bot is None:
            kwargs = dict()
            if self._base_url:
                kwargs['base_url'] = self._base_url
            self._bot = Bot(self._token, **kwargs)
        return self._bot

    def get_dispatcher(self):
        if self._dispatcher is None:
            self._dispatcher = Dispatcher(
                self.get_bot(),
                use_context=True,
                update_queue=None, workers=0
            )
            for command, handler in handlers.items():
                self._dispatcher.add_handler(CommandHandler(command, handler))
            self._dispatcher.add_error_handler(self._error_handler)
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

    def process_update(self, json_text):
        update = Update.de_json(json.loads(json_text), self.get_bot())
        return self.get_dispatcher().process_update(update)

    @classmethod
    def get_bot_endpoint(cls):
        return 'https://api.telegram.org/bot{}'.format(cls._token)

    @classmethod
    def get_webhook_url(cls):
        return cls._webhook_url

    @classmethod
    def get_bot_contact_link(cls):
        instance = cls()
        return 'https://t.me/{0}'.format(instance.get_bot().username)


class TelegramRenderer(BaseRenderer):
    def __init__(self, domain):
        BaseRenderer.__init__(self)
        self.domain = domain

    def render_notification(self, user_profile, unread_messages):
        with enable_translation(user_profile):
            user = user_profile.user

            unread_count = len(unread_messages)
            unread_count_string = self._get_string(unread_count)

            context = {
                "domain": self.domain,
                "user": user,
                "unread_count": unread_count,
                "unread_count_string": unread_count_string,
                "messages": list(zip(range(1, unread_count + 1), unread_messages))
            }

            markdown = render_to_string('tg_notification_mail.md', context).strip()
            rendered_message = (markdown, user_profile.telegram_uid)

        return rendered_message

    def render_fulltext(self, message, recipients):
        return 'Rendered fulltext stub'


class TelegramSender(BaseSender):
    def mass_send(self, prepared_messages):
        logger.info('TelegramSender.mass_send stub:', prepared_messages)
        return 0
