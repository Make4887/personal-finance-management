"""Модели данных проекта"""
from django.db import models
from django.contrib.auth.models import User


class UserAccounts(models.Model):
    """Модель счёта"""
    account_id = models.AutoField(primary_key=True, auto_created=True)
    nameofuser = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None)
    account_name = models.CharField(max_length=200)
    account_start_balance = models.FloatField(default=0.0)
    account_start_date = models.DateTimeField(auto_now_add=True)
    account_current_balance = models.FloatField(default=0.0)
    account_new = models.BooleanField(default=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __int__(self):
        return self.account_id


class Transaction(models.Model):
    """Модель транзакции"""
    account_id = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    is_income = models.BooleanField(default=False)
    is_expense = models.BooleanField(default=False)
    is_transfer = models.BooleanField(default=False)
    amount = models.FloatField(default=0.0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    transaction_id = models.AutoField(primary_key=True, auto_created=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    transfer_account_id = models.IntegerField(blank=True, null=True)
    trans_acc_name = models.CharField(max_length=500, blank=True, null=True)

    def __float__(self):
        return self.amount
