# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 17:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('sender', models.CharField(max_length=500)),
                ('receiver', models.CharField(max_length=500)),
                ('subject', models.CharField(max_length=500)),
                ('html_body', models.TextField(blank=True, null=True)),
                ('text_body', models.TextField(blank=True, null=True)),
                ('job_id', models.CharField(max_length=500)),
                ('status', models.CharField(blank=True, max_length=20)),
                ('exception_stacktrace', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('url', models.CharField(max_length=500)),
                ('stacktrace', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
