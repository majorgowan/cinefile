# Generated by Django 5.1 on 2024-09-15 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_rename_film_id_viewing_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewing',
            name='video_medium',
            field=models.CharField(blank=True, max_length=9),
        ),
        migrations.AlterField(
            model_name='viewing',
            name='comments',
            field=models.TextField(blank=True, max_length=4096),
        ),
    ]
