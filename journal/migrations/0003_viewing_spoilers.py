# Generated by Django 5.1 on 2024-11-21 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewing',
            name='spoilers',
            field=models.BooleanField(default=False),
        ),
    ]
