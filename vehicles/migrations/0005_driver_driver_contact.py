# Generated by Django 5.1.3 on 2024-12-10 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0004_rename_drivery_status_driver_driver_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driver_contact',
            field=models.IntegerField(default='9999999999', unique=True),
        ),
    ]