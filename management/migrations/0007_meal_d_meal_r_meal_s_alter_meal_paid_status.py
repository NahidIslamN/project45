# Generated by Django 5.0.6 on 2024-06-26 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_notification_seen_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='D',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='R',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='S',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='meal',
            name='paid_status',
            field=models.BooleanField(default=True),
        ),
    ]
