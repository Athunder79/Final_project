# Generated by Django 5.0.1 on 2024-03-01 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_coordinates_club'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinates',
            name='shot_number',
        ),
    ]