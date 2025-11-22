
import os
from pathlib import Path

from dotenv import load_dotenv
from decouple import config

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = config("SECRET_KEY", cast=str)


DEBUG = False

SITE_ID = 3

ALLOWED_HOSTS = ["example.com", "localhost", "127.0.0.1"]


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
    'apps.users',
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


# AUTH

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Какие методы входа разрешены
ACCOUNT_LOGIN_METHODS = {"email", "username"}  


# Какие поля показывать на регистрации
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

ACCOUNT_FORMS = {
    'login': 'apps.users.forms.CustomLoginForm',
    'signup': 'apps.users.forms.CustomSignupForm',
}


SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True 

ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # подтверждение email обязательно
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "goodfood:main"  # куда кидать после подтверждения
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter' # Это нужно, чтобы allauth не конфликтовал с кастомными шаблонами

LOGIN_REDIRECT_URL = "goodfood:main"  # куда кидать после входа
LOGOUT_REDIRECT_URL = "goodfood:main"  # куда после выхода

# EMAIL
EMAIL_BACKEND = f'{config("EMAIL_BACKEND", cast=str)}'

# SMTP-сервер и порт
EMAIL_HOST = f'{config("EMAIL_HOST", cast=str)}'  
EMAIL_PORT = f'{config("EMAIL_PORT", cast=int)}'            

EMAIL_USE_TLS = f'{config("EMAIL_USE_TLS", cast=bool)}'

EMAIL_HOST_USER = f'{config("EMAIL_HOST_USER", cast=str)}'
EMAIL_HOST_PASSWORD = f'{config("EMAIL_HOST_PASSWORD", cast=str)}'

# Адрес отправителя по умолчанию
DEFAULT_FROM_EMAIL = f'{config("DEFAULT_FROM_EMAIL", cast=str)}'