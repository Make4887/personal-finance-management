"""Формы проекта"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserAccounts, Transaction


class RegisterForm(UserCreationForm):
    """Регистрационная форма"""
    class Meta(UserCreationForm.Meta):
        """Мета-класс регистрационной формы"""
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


class AddAccountForm(forms.ModelForm):
    """Форма добавления счета"""
    class Meta:
        """Мета-класс формы добавления счета"""
        model = UserAccounts
        fields = ('nameofuser', 'account_name', 'account_start_balance')


class AddTransactionForm(forms.ModelForm):
    """Форма добавления транзакции"""
    class Meta:
        """Мета-класс формы добавления транзакции"""
        model = Transaction
        fields = ('is_income', 'is_expense',
                  'is_transfer', 'amount', 'description',
                  'category', 'transfer_account_id')
