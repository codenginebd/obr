# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcategory',
            name='slug',
            field=models.SlugField(default=None),
            preserve_default=False,
        ),
    ]
