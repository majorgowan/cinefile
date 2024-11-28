# Generated by Django 5.1 on 2024-11-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_viewing_spoilers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewing',
            name='cinema',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='viewing',
            name='location',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='viewing',
            name='streaming_platform',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='viewing',
            name='tv_channel',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
