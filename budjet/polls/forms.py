from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class AddAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccounts
        fields = ('nameofuser', 'account_name', 'account_start_balance')


class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('is_income', 'is_expense', 'is_transfer', 'amount', 'description', 'category', 'transfer_account_id')
