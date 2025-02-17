# Generated by Django 5.0.6 on 2024-06-25 11:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0012_alter_customuser_otp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_nmber', models.CharField(max_length=15, unique=True)),
                ('is_veryfied', models.BooleanField(default=False)),
                ('balance', models.FloatField(default=0.0)),
                ('balance_chal', models.FloatField(default=0.0)),
                ('if_manager', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateField(auto_now=True)),
                ('Hostel_account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Accounts.holteluser')),
                ('Manager_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.holtelmanager')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('discription', models.TextField()),
                ('bill_amount', models.FloatField()),
                ('last_date_of_payment', models.DateField()),
                ('jorimana', models.FloatField(default=100.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateField(auto_now=True)),
                ('bill_creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Accounts.holtelmanager')),
                ('payment_user', models.ManyToManyField(related_name='paymentof_bills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_chrge', models.FloatField()),
                ('meal_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateField(auto_now=True)),
                ('paid_status', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.holtelmanager')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateField(auto_now=True)),
                ('recever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Accounts.holtelmanager')),
            ],
        ),
    ]
