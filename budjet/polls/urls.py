from django.urls import path

from . import views
from .views import profile_view, RegisterView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about/', views.about, name='about'),
    path("profile/", profile_view, name='profile'),
    path('<int:account_id>/delete_account/', views.delete_account, name='delete_account'),
    path('<int:account_id>/edit_account/', views.edit_account, name='edit_account'),
    path('<int:account_id>/add_transaction/', views.add_transaction, name='add_transaction'),
    path("profile/<int:account_id>/history_accounts", views.history_accounts, name='history_accounts'),
    path('<int:transaction_id>/delete_transaction/', views.delete_transaction, name='delete_transaction'),
    ]