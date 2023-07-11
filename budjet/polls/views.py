import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import *
from .models import UserAccounts
from django.core.exceptions import ValidationError


# Отображение основной страницы
def index(request):
    return render(request, "polls/landing/index.html")


# Отображение регистрационной формы и переход к профилю при успешной регистрации
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("polls:profile")

    # Проверка формы
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# Отображение страницы описания
def about(request):
    return render(request, "polls/landing/about.html")


# Отображение профиля со счетами с проверкой входа пользователя
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.nameofuser = request.user
            instance.account_current_balance = request.POST.get('account_start_balance')
            instance.save()
            return redirect('profile')
    user_accounts = UserAccounts.objects.order_by('account_start_date')
    acc_quantity = 0
    profile_balance = 0
    for each in user_accounts:
        if each.nameofuser_id == request.user.id and not each.is_deleted:
            acc_quantity += 1
            profile_balance += each.account_current_balance
    return render(request, 'polls/profile/profile.html', {
        'user_accounts': user_accounts,
        'acc_quantity': acc_quantity,
        'profile_balance': profile_balance
    })


@login_required
def add_transaction(request, account_id):
    if request.method == 'POST':
        form = AddTransactionForm(request.POST)
        user_account = UserAccounts.objects.get(account_id=account_id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.account_id = UserAccounts.objects.get(pk=account_id)
            if instance.is_expense:
                instance.amount = -float(request.POST.get('amount'))
                user_account.account_current_balance -= float(request.POST.get('amount'))
            elif instance.is_income:
                user_account.account_current_balance += float(request.POST.get('amount'))
            elif instance.is_transfer:
                transfer_account = UserAccounts.objects.get(account_id=instance.transfer_account_id)
                transfer_account.account_current_balance += float(request.POST.get('amount'))
                user_account.account_current_balance -= float(request.POST.get('amount'))
                instance.trans_acc_name = user_account.account_name
                transfer_account.save()
            user_account.account_new = False
            user_account.save()
            instance.save()

            return redirect('profile')
        else:
            # Do something in case if form is not valid
            raise ValidationError(form.errors)

    # account_transaction = Transaction.objects.all()
    return render(request, 'polls/profile/profile.html')


def delete_account(request, account_id):
    account = UserAccounts.objects.get(pk=account_id)
    account.is_deleted = True
    account.save()
    return redirect('profile')


@login_required
def edit_account(request, account_id):
    account = UserAccounts.objects.get(pk=account_id)
    if request.method == 'POST':
        account.account_name = request.POST.get('account_name')
        if account.account_new:
            account.account_start_balance = request.POST.get('account_start_balance')
            account.account_current_balance = request.POST.get('account_start_balance')
        account.save()
        return redirect('profile')
    else:
        return render(request, 'profile.html')


@login_required
def history_accounts(request, account_id):
    transactions = Transaction.objects.filter(account_id=account_id)
    transfer_transactions = Transaction.objects.filter(transfer_account_id=account_id)
    trans_list = transactions | transfer_transactions
    account = UserAccounts.objects.get(pk=account_id)
    transfer_accounts = UserAccounts.objects.filter(nameofuser=account.nameofuser)
    chart_amount = [0, 0, 0, 0]
    for i in trans_list:
        if i.is_expense:
            chart_amount[0] -= i.amount
        elif i.is_income:
            chart_amount[1] += i.amount
        elif i.is_transfer and i.transfer_account_id == account_id:
            chart_amount[3] += i.amount
        elif i.is_transfer and i.account_id.account_id == account_id:
            chart_amount[2] += i.amount

    income_amount = []
    income_category = []
    for i in trans_list:
        if i.is_income:
            income_category.append(str(i.category).title())
        elif i.is_transfer and i.transfer_account_id == account_id:
            income_category.append("Переводы на счет")
    income_category = list(set(income_category))
    for i in income_category:
        income_amount.append(0)
    for i in trans_list:
        for a in income_category:
            if i.is_income and str(i.category).title() == a:
                income_amount[income_category.index(a)] += float(i.amount)
        if i.is_transfer and i.transfer_account_id == account_id:
            income_amount[income_category.index("Переводы на счет")] += float(i.amount)
    income_category = json.dumps(income_category)

    expense_amount = []
    expense_category = []
    for i in trans_list:
        if i.is_expense:
            expense_category.append(str(i.category).title())
        elif i.is_transfer and i.account_id.account_id == account_id:
            expense_category.append("Переводы со счета")
    expense_category = list(set(expense_category))
    for i in expense_category:
        expense_amount.append(0)
    for i in trans_list:
        for a in expense_category:
            if i.is_expense and str(i.category).title() == a:
                expense_amount[expense_category.index(a)] -= float(i.amount)
        if i.is_transfer and i.account_id.account_id == account_id:
            expense_amount[expense_category.index("Переводы со счета")] += float(i.amount)
    expense_category = json.dumps(expense_category)

    daily_balance_change = {account.account_start_date.date().strftime('%d/%m/%y'): account.account_start_balance}
    trans_list = trans_list.order_by('transaction_date')
    transactions_amount = len(trans_list)
    for i in range(transactions_amount):
        if trans_list[i].transaction_date.date().strftime('%d/%m/%y') not in daily_balance_change.keys():
            daily_balance_change.update({trans_list[i].transaction_date.date().strftime('%d/%m/%y'): 0})
        if trans_list[i].is_transfer and trans_list[i].account_id.account_id == account_id:
            daily_balance_change[trans_list[i].transaction_date.date().strftime('%d/%m/%y')] -= trans_list[i].amount
        else:
            daily_balance_change[trans_list[i].transaction_date.date().strftime('%d/%m/%y')] += trans_list[i].amount
    balance_change = list(daily_balance_change.values())
    for i in range(len(balance_change) - 1):
        balance_change[i + 1] += balance_change[i]
    changing_date = json.dumps(list((daily_balance_change.keys())))


    return render(request, 'polls/profile/history_accounts.html',
                  {'trans_list': trans_list, 'account': account, 'transfer_accounts': transfer_accounts,
                   'chart_amount': chart_amount, 'income_category': income_category,
                   'income_amount': income_amount,  'expense_category': expense_category,
                   'expense_amount': expense_amount, 'balance_change': balance_change,
                   'changing_date': changing_date, 'transactions_amount': transactions_amount, }, )


def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    account_id = int(transaction.account_id)
    user_account = UserAccounts.objects.get(account_id=account_id)
    if transaction.is_expense:
        user_account.account_current_balance -= transaction.amount
    elif transaction.is_income:
        user_account.account_current_balance -= transaction.amount
    elif transaction.is_transfer:
        transfer_account = UserAccounts.objects.get(account_id=transaction.transfer_account_id)
        transfer_account.account_current_balance -= transaction.amount
        user_account.account_current_balance += transaction.amount
        transfer_account.save()

    user_account.save()
    transaction.delete()

    return redirect('history_accounts', account_id)


def edit_transaction(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    user_account = UserAccounts.objects.get(account_id=transaction.account_id)
    account_id = int(transaction.account_id)
    if request.method == 'POST':
        if transaction.is_expense or transaction.is_income:
            user_account.account_current_balance -= float(transaction.amount)
            transaction.amount = request.POST.get('amount')
            transaction.category = request.POST.get('category')
            transaction.description = request.POST.get('description')
            user_account.account_current_balance += float(transaction.amount)
        elif transaction.is_transfer:
            transfer_account = UserAccounts.objects.get(account_id=transaction.transfer_account_id)
            user_account.account_current_balance += float(transaction.amount)
            transfer_account.account_current_balance -= float(transaction.amount)
            transaction.amount = request.POST.get('amount')
            transaction.description = request.POST.get('description')
            transfer_account.save()
            transaction.transfer_account_id = request.POST.get('transfer_account_id')
            user_account.account_current_balance -= float(transaction.amount)
            transfer_account_new = UserAccounts.objects.get(account_id=transaction.transfer_account_id)
            transfer_account_new.account_current_balance += float(transaction.amount)
            transaction.trans_acc_name = transfer_account_new.account_name
            transfer_account_new.save()

        transaction.save()
        user_account.save()
    return redirect('history_accounts', account_id)


@login_required
def edit_profile(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.save()
        return redirect('profile')
    else:
        return render(request, 'profile.html')
