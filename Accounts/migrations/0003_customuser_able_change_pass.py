# Generated by Django 5.0.6 on 2024-06-14 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_customuser_active_status_customuser_adress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='able_change_pass',
            field=models.BooleanField(default=False),
        ),
    ]
