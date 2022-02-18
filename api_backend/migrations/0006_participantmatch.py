# Generated by Django 4.0.2 on 2022-02-15 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0005_alter_participant_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.BooleanField(null=True, verbose_name='Совпадение')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_match', to='api_backend.participant', verbose_name='Участник')),
            ],
        ),
    ]
