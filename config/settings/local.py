from .base import *
from decouple import config
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Основные настройки локальной среды
# ----------------------------
SITE_ID = 3
DEBUG = True
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["*"]
STATIC_ROOT = BASE_DIR / "static_collect"

# ----------------------------
# Email для разработки
# ----------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ----------------------------
# Database (PostgreSQL локальная)
# ----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

# ----------------------------
# Cache локальный
# ----------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "local-cache",
    }
}

# ----------------------------
# Debug Toolbar
# ----------------------------
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}

# ----------------------------
# WhiteNoise 
# ----------------------------
MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ----------------------------
# CSP (только для локала)
# ----------------------------
CSP_MIDDLEWARE = []
CSP_REPORT_ONLY = True
