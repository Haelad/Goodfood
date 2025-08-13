
import os
from pathlib import Path

from dotenv import load_dotenv
from decouple import config

load_dotenv()

# Time settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY", cast=str)

DEBUG = True

ALLOWED_HOSTS = ["localhost","127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1","localhost"]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.py"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.goodfood', 
] 


# создать MIDDLEWARE для отработки исключений и прочего
MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{config("REDIS_HOST", "REDIS_PASSWORD")}/0',  
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}





# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/



DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S', # Стандартный формат (24-часовой) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
    '%m/%d/%Y %I:%M %p', # Формат в американском стиле (12-часовой с AM/PM) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
    '%d-%b-%Y %H:%M:%S', # Формат в европейском стиле (день-месяц-год) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
)



USE_TZ = True
YEAR_MONTH_FORMAT = "m/Y"

USE_THOUSAND_SEPARATOR = None


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT= os.path.join(BASE_DIR,'static_collect')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
