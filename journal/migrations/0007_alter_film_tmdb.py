# Generated by Django 5.1 on 2024-09-27 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0006_importedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='tmdb',
            field=models.IntegerField(unique=True),
        ),
    ]
