"""Настройки приложения"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Конфиг приложения"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
