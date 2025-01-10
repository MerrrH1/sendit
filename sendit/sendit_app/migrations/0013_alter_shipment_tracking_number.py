# Generated by Django 5.1.4 on 2024-12-23 14:55

import sendit_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendit_app', '0012_alter_shipment_courier_alter_shipment_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='tracking_number',
            field=models.CharField(default=sendit_app.models.get_tracking_number, editable=False, max_length=20, unique=True),
        ),
    ]
