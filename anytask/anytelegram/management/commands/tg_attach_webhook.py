# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from anytask.anytelegram.common import AnyTelegram


class Command(BaseCommand):
    """Calls setWebhook method"""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.api = AnyTelegram()
        self.bot_endpoint = AnyTelegram.get_webhook_url()
        self.webhook_url = AnyTelegram.get_webhook_url()

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
        webhook_info = self.api.get_bot().get_webhook_info()
        self.stdout.write('webhookInfo: {}'.format(webhook_info))
        set_success = self.api.set_webhook(drop_pending_updates=options['drop_pending_updates'])
        if not set_success:
            self.stdout.write('Setting webhook failed')
        else:
            self.stdout.write('Webhook set, no errors')
