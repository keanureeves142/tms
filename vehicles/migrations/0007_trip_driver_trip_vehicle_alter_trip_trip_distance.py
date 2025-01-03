# Generated by Django 5.1.3 on 2024-12-10 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_trip_alter_driver_driver_contact_adhoccost'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='driver',
            field=models.ForeignKey(default='DR000001', limit_choices_to={'driver_status': 'active'}, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='vehicles.driver'),
        ),
        migrations.AddField(
            model_name='trip',
            name='vehicle',
            field=models.ForeignKey(default='KA02M1221', limit_choices_to={'status': 'active'}, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='vehicles.vehicle'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='trip_distance',
            field=models.FloatField(default='0'),
        ),
    ]
