# Generated by Django 5.0.1 on 2024-03-25 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_hole_hole_num_alter_hole_hole_par'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='shot_distance',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True),
        ),
    ]
