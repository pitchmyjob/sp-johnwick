# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0002_ask_receivers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ask',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
