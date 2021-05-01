from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import logging

logger = logging.getLogger('django.request')


@csrf_exempt
@require_POST
def webhook(request, token):
    logger.error('anytelegram webhook stub: token=%s request=%s', token, request.body)
    return HttpResponse(status=200)
