# Generated by Django 5.1 on 2024-11-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_juser_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='juser',
            name='displayname',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]