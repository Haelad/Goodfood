from .base import *
from dotenv import load_dotenv
from decouple import config

load_dotenv()

DEBUG = True
ALLOWED_HOSTS = ["*"]




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


# Статические файлы прямо из /static/
STATICFILES_DIRS = [BASE_DIR / "static"]