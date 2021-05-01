# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
import requests

from anytask.anytelegram.common import bot_endpoint


class Command(BaseCommand):
    """Calls deleteWebhook method"""

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__()
        token = settings.TELEGRAM_TOKEN
        self.bot_endpoint = bot_endpoint(token)

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
        if webhook_info.status_code == 200:
            pass
        elif webhook_info.status_code == 404:
            self.stdout.write('No webhook was attached, nothing changed')
            return
        else:
            self.stdout.write('webHookInfo failed, exiting')
            return

        delete_result = requests.post(
            self.bot_endpoint + '/deleteWebhook',
            params={'drop_pending_updates': options['drop_pending_updates']}
        )
        self.stdout.write('deleteWebhook: {} {}'.format(delete_result.status_code, delete_result.text))
        if delete_result.status_code != 200:
            self.stdout.write('deleteWebhook failed, exiting')
            return

        self.stdout.write('Webhook deleted, no errors')
