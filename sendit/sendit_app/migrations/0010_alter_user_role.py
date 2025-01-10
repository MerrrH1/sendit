# Generated by Django 5.1.4 on 2024-12-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendit_app', '0009_shipment_review_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('courier', 'Courier')], default='courier', max_length=15),
        ),
    ]
