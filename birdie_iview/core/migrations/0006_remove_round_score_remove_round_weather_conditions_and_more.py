# Generated by Django 5.0.1 on 2024-03-06 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_round_round_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='score',
        ),
        migrations.RemoveField(
            model_name='round',
            name='weather_conditions',
        ),
        migrations.RemoveField(
            model_name='shot',
            name='round',
        ),
    ]