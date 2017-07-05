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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=500)),
                ('subtitle', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=500)),
                ('slug', models.SlugField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.BookCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookEdition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('isbn', models.CharField(blank=True, max_length=500)),
                ('edition', models.CharField(max_length=100)),
                ('publish_date', models.DateField(null=True)),
                ('page_count', models.IntegerField(default=0)),
                ('is_used', models.BooleanField(default=False)),
                ('authors', models.ManyToManyField(to='book.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookUploadHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('file_name', models.CharField(max_length=500)),
                ('total_count', models.IntegerField(default=0)),
                ('new_uploaded', models.IntegerField(default=0)),
                ('sheet', models.CharField(max_length=500)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=10)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bauth.Country')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=20)),
                ('short_name', models.CharField(max_length=10)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bauth.Country')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriceConfigUpdateHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('value_p', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('value_v', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('special_price', models.BooleanField(default=False)),
                ('book_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookEdition')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PriceCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('initial_payable_rent', models.DecimalField(decimal_places=2, max_digits=20)),
                ('initial_payable_buy', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Currency')),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('days', models.IntegerField(default=1)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RentPriceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('value_p', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('value_v', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('special_price', models.BooleanField(default=False)),
                ('book_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookEdition')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.RentPlan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('date_created', models.BigIntegerField()),
                ('last_updated', models.BigIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='priceconfigupdatehistory',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.RentPlan'),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='base_prices',
            field=models.ManyToManyField(to='book.PriceCurrency'),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book'),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Language'),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.BookPublisher'),
        ),
        migrations.AddField(
            model_name='bookedition',
            name='tags',
            field=models.ManyToManyField(to='book.TagKeyword'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.BookCategory'),
        ),
        migrations.AddField(
            model_name='book',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
