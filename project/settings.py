
import os
from pathlib import Path

from dotenv import load_dotenv
from decouple import config

load_dotenv()

# Time settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = [str(hts) for hts in config("ALLOWED_HOSTS").split(",")]

INTERNAL_IPS = [str(ips) for ips in config("INTERNAL_IPS").split(",")]

# CSP
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)  # разрешённые источники для JS
CSP_STYLE_SRC = ("'self'",)  # разрешённые источники для CSS
CSP_FONT_SRC = ("'self'",) # разрешенные источники для шрифтов
CSP_IMG_SRC = ("'self'", 'data:') # разрешенные источники для изображений
CSP_CONNECT_SRC = ("'self'",) # разрешенные источники для подключений
CSP_REPORT_URI = None # адрес сервера для логов



# КУКИ
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
# ФИЛЬТРЫ
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
# РАЗРЕШЕННИЯ 
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_CROSS_ORIGIN_RESOURCE_POLICY = 'same-site'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = 'require-corp'
SESSION_COOKIE_SAMESITE = 'Lax'
# HSTS
SECURE_HSTS_SECONDS = 31536000 # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'goodfood', 
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

ROOT_URLCONF =  config("ROOT_URLCONF")

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
        "LOCATION": f'redis://{config("REDIS_HOST", "REDIS_PASSWORD")}/0',  # Use the Redis service name from docker-compose
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

WSGI_APPLICATION = config("WSGI_APPLICATION")



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

LANGUAGE_CODE = 'ru'

DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S', # Стандартный формат (24-часовой) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
    '%m/%d/%Y %I:%M %p', # Формат в американском стиле (12-часовой с AM/PM) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
    '%d-%b-%Y %H:%M:%S', # Формат в европейском стиле (день-месяц-год) [1](https://runebook.dev/en/articles/django/ref/settings/std:setting-DATETIME_INPUT_FORMATS)
)



USE_TZ = config("USE_TZ", cast=bool)

YEAR_MONTH_FORMAT = config("YEAR_MONTH_FORMAT")

USE_THOUSAND_SEPARATOR = None


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = config("STATIC_URL")

STATIC_ROOT= os.path.join(BASE_DIR,'static_collect')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = config("MEDIA_URL")

# Путь хранения картинок
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
