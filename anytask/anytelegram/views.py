from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import settings
from common import AnyTelegram

import logging

logger = logging.getLogger('django.request')

api = AnyTelegram()


@csrf_exempt
@require_POST
def webhook(request, token):
    """https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#alternative-no-threading"""
    if token != settings.TELEGRAM_WEBHOOK_SECRET:
        logger.warn('Invalid webhook endpoint token: %s', token)
        return HttpResponseForbidden()
    logger.error(request.body)
    logger.error(api.process_update(request.body))
    return HttpResponse(status=200)
