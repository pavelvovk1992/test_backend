# Generated by Django 4.0.2 on 2022-02-13 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='email',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='last_name',
        ),
    ]