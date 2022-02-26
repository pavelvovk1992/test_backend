# Generated by Django 4.0.2 on 2022-02-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0016_participant_latitude_participant_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantmatch',
            name='match',
        ),
        migrations.RemoveField(
            model_name='participantmatch',
            name='participant',
        ),
        migrations.AddField(
            model_name='participantmatch',
            name='participant',
            field=models.ManyToManyField(null=True, to='api_backend.Participant', verbose_name='Участник'),
        ),
    ]