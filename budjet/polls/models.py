from email.policy import default

from django.db import models
from django.contrib.auth.models import User


#Модель счёта
class UserAccounts(models.Model):
    account_id = models.AutoField(primary_key=True, auto_created=True)
    nameofuser = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, default=None)
    account_name = models.CharField(max_length=200)
    account_start_balance = models.FloatField(default=0.0)
    account_start_date = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.account_id


#Модель транзакции
class Transaction(models.Model):
    account_id = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    is_income = models.BooleanField(default=False)
    is_expense = models.BooleanField(default=False)
    is_transfer = models.BooleanField(default=False)
    amount = models.FloatField(default=0.0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, default='')
    transaction_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200, default='')
    account_current_balance = models.FloatField(default=0.0)
    transfer_account_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.amount
