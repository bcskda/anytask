__{% load i18n %}{% trans "u_vas_soobshenij" %} {{ unread_count }} {{ unread_count_string }}__
{% trans "posmotret_soobshenija" %}:
{{ domain }}{% url "mail.views.mail_page" %}
{% for index, message in messages %}{{ index }}. {{ message.sender.get_full_name }} -- _{{ message.title }}_
{% endfor %}