# Generated by Django 5.0.1 on 2024-03-23 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_shot_end_latitude_shot_end_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hole',
            name='hole_num',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='hole',
            name='hole_par',
            field=models.IntegerField(),
        ),
    ]
