from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# SQLite для простоты разработки
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Статические файлы прямо из /static/
STATICFILES_DIRS = [BASE_DIR / "static"]