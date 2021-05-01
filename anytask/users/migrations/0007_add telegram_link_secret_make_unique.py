# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-01 19:25
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_add telegram_link_secret_fill_uuids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='telegram_link_secret',
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=False),
        )
    ]
