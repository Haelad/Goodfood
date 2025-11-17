
import os
from pathlib import Path

from dotenv import load_dotenv
from decouple import config

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = config("SECRET_KEY", cast=str)


DEBUG = False

SITE_ID = 1

ALLOWED_HOSTS = ["localhost","127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1","localhost"]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


STATIC_URL = "/static/"
STATIC_ROOT= os.path.join(BASE_DIR,'static_collect')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'apps.goodfood',
    'widget_tweaks', 
]
     

MIDDLEWARE = [
    # --- Безопасность и статические файлы ---
    'django.middleware.security.SecurityMiddleware',

    # --- Сессии, куки, запросы ---
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # --- Аутентификация и учетные записи ---
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    # --- Сообщения и шаблоны ---
    'django.contrib.messages.middleware.MessageMiddleware',

    # --- CSP и защита от iframe ---
    'csp.middleware.CSPMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S', # Стандартный формат (24-часовой) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
    '%m/%d/%Y %I:%M %p', # Формат в американском стиле (12-часовой с AM/PM) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
    '%d-%b-%Y %H:%M:%S', # Формат в европейском стиле (день-месяц-год) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
)


USE_TZ = True
YEAR_MONTH_FORMAT = "m/Y"

# USE_THOUSAND_SEPARATOR = None


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


