# Generated by Django 4.2.2 on 2023-06-18 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('account_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('account_name', models.CharField(default='', max_length=200)),
                ('account_start_balance', models.FloatField(default=0.0)),
                ('account_start_date', models.DateTimeField(auto_now_add=True)),
                ('nameofuser', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('is_income', models.BooleanField(default=False)),
                ('is_expense', models.BooleanField(default=False)),
                ('is_transfer', models.BooleanField(default=False)),
                ('amount', models.FloatField(default=0.0)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(default='', max_length=500)),
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(default='', max_length=200)),
                ('account_current_balance', models.FloatField(default=0.0)),
                ('transfer_account_id', models.IntegerField(blank=True, null=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.useraccounts')),
            ],
        ),
    ]