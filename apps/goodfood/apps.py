from django.apps import AppConfig


class GoodfoodConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.goodfood"

    def ready(self):
        # Регистрирует обработчики: права новым пользователям и сброс кэша
        from . import signals  # noqa: F401
