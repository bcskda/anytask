# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
import requests

from anytask.anytelegram.common import bot_endpoint


class Command(BaseCommand):
    """Calls setWebhook method"""

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__()
        token = settings.TELEGRAM_TOKEN
        self.bot_endpoint = bot_endpoint(token)
        self.webhook_url = settings.TELEGRAM_WEBHOOK_URL

    def add_arguments(self, parser):
        """Call super when overriding"""
        parser.add_argument(
            '--drop-pending-updates',
            dest='drop_pending_updates',
            action='store_true',
            default=False,
            help='Ask API to drop pending updates'
        )

    def handle(self, **options):
        webhook_info = requests.get(self.bot_endpoint + '/webhookInfo')
        self.stdout.write('webhookInfo: {} {}'.format(webhook_info.status_code, webhook_info.text))

        set_result = requests.post(
            self.bot_endpoint + '/setWebhook',
            params={
                'url': self.webhook_url,
                'drop_pending_updates': options['drop_pending_updates']
            }
        )
        self.stdout.write('setWebhook: {} {}'.format(set_result.status_code, set_result.text))
        if set_result.status_code != 200:
            self.stdout.write('setWebhook failed, exiting')
            return

        self.stdout.write('Webhook set, no errors')
