# Generated by Django 5.0.1 on 2024-03-01 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_coordinates_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinates',
            name='updated_at',
        ),
    ]