# Generated by Django 5.1.4 on 2024-12-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendit_app', '0005_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
