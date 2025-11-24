from .base import *

from decouple import config

load_dotenv()

DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"




INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
} 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': f'{config("POSTGRES_DB")}',
        'USER': f'{config("POSTGRES_USER")}',
        'PASSWORD': f'{config("POSTGRES_PASSWORD")}',
        'HOST': f'{config("POSTGRES_HOST")}',
        'PORT': f'{config("POSTGRES_PORT")}',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "local-cache",
    }
}



# Статические файлы прямо из /static/
STATICFILES_DIRS = [str(BASE_DIR / "static")]

