import anytelegram.views
from django.conf.urls import url

urlpatterns = [
    url(r'^webhook/(?P<token>[0-9a-zA-Z_:\-\+]+)$', anytelegram.views.webhook,
        name='anytelegram.views.webhook')
]
