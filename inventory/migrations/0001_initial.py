# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 17:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bauth', '0001_initial'),
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookWarehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=500)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bauth.Adress')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WarehouseInventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('stock', models.BigIntegerField(default=0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookEdition')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.BookWarehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]