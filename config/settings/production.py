from .base import *

import os

from decouple import config
from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Основные настройки продакшн
# ----------------------------
DEBUG = False
SECRET_KEY = config("SECRET_KEY")
SITE_ID = 1
ALLOWED_HOSTS = ["goodhealthyfood.ru", "goodhealthyfood.online"]
STATIC_ROOT = os.path.join(BASE_DIR, "static_collect")

# ----------------------------
# Database (PostgreSQL прод)
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
# Cache (Redis)
# ----------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{config("REDIS_HOST")}:{config("REDIS_PORT")}/0',
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# ----------------------------
# Статика и медиа
# ----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_collect")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ----------------------------
# Security / CSP
# ----------------------------
CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "style-src": ["'self'"],
    "font-src": ["'self'"],
    "img-src": ["'self'", "data:"],
    "connect-src": ["'self'"],
}

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_RESOURCE_POLICY = "same-site"
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = "require-corp"

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ----------------------------
# Email для продакшн
# ----------------------------
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# ----------------------------
# Logging
# ----------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "file_django": {
            "level": "DEBUG",
            "formatter": "simple",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "config/logs/django.txt"),
        },
        "file": {
            "level": "WARNING",
            "formatter": "verbose",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "config/logs/logs.txt"),
        },
        "mail": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "django": {"handlers": ["file_django"], "level": "DEBUG", "propagate": False},
        "thread": {"handlers": ["file"], "level": "WARNING", "propagate": False},
        "mail_thread": {"handlers": ["mail"], "level": "ERROR", "propagate": False},
    },
}
