# Generated by Django 4.0.2 on 2022-02-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0020_alter_participant_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='match_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]