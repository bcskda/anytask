# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from anytask.anytelegram.common import AnyTelegram


class Command(BaseCommand):
    """Calls deleteWebhook method"""

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__()
        self.api = AnyTelegram()

    def handle(self, **options):
        webhook_info = self.api.get_bot().get_webhook_info()
        self.stdout.write('webhookInfo: {}'.format(webhook_info))
        delete_success = self.api.delete_webhook()
        if not delete_success:
            self.stdout.write('Deleting webhook failed, exiting')
        else:
            self.stdout.write('Webhook deleted, no errors')
