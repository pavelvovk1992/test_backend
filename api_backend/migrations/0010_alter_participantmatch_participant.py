# Generated by Django 4.0.2 on 2022-02-15 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0009_alter_participantmatch_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantmatch',
            name='participant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_backend.participant', verbose_name='Участник'),
        ),
    ]
