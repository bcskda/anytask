# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-14 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_add telegram_link_secret_make_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='show_telegram',
            field=models.BooleanField(default=False),
        ),
    ]