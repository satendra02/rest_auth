# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-23 14:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rest_auth',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
