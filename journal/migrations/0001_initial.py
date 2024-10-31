# Generated by Django 5.1 on 2024-09-09 16:51

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb', models.IntegerField()),
                ('title', models.CharField(max_length=64)),
                ('year', models.IntegerField()),
                ('director', models.CharField(max_length=32)),
                ('starring', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Viewing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('city', models.CharField(blank=True, max_length=32)),
                ('cinema_or_tv', models.CharField(blank=True, max_length=7)),
                ('tv_channel', models.CharField(blank=True, max_length=16)),
                ('cinema', models.CharField(blank=True, max_length=32)),
                ('comments', models.TextField(blank=True, max_length=2048)),
                ('film_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='viewings', to='journal.film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]