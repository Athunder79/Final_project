# Generated by Django 5.0.1 on 2024-03-13 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_shot_hole_num_remove_shot_hole_par_hole_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shot',
            name='hole_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shot',
            name='hole_par',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]