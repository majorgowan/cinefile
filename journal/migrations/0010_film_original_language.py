# Generated by Django 5.1 on 2024-10-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0009_alter_viewing_cinema_or_tv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='original_language',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
