# Generated by Django 5.1.3 on 2024-12-09 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_driver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='drivery_status',
            new_name='driver_status',
        ),
    ]
