
from .base import *
from dotenv import load_dotenv
from decouple import config


load_dotenv()

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{config("REDIS_HOST", "REDIS_PASSWORD")}/0',  # Use the Redis service name from docker-compose
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {message}", # форматор, определяет какие данные будут в логах
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{" # обзначает синтаксис подстонвки данных в форматор
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}", 
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{" 
        }
    },
    
    "filters": {
    "require_debug_false": {
        "()": "django.utils.log.RequireDebugFalse"
    }
    },
    "handlers": {
        "file_django": {
            "level": "DEBUG",
            "formatter": "simple",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "config/logs", "django.txt")
        },
        "file": {
            "level": "WARNING",
            "formatter": "verbose",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "config/logs", "logs.txt")
        },
        "mail": {
            "level":  "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
            "filters": ["require_debug_false"], 
            
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_django"],
            "level": "DEBUG",
            "propagate": False
        },
        "thread":{
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "mail_thread" : {
            "handlers": ["mail"],
            "level": "ERROR",
            "propagate": False,
        }
    },
}

# security
DEBUG = False

SECRET_KEY = config("SECRET_KEY", cast=str)

ALLOWED_HOSTS = ['haeladgoodfood.ru', 'www.haeladgoodfood.ru']
#Domen2025 Hosting2025 Webconstr2025


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
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = "/static/"
STATIC_ROOT= os.path.join(BASE_DIR,'static_collect')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

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
    'login': 'goodfood.forms.CustomLoginForm',
    'signup': 'goodfood.forms.CustomSignupForm',
}



SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True 

ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # подтверждение email обязательно

ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "goodfood:main"  # куда кидать после подтверждения
LOGIN_REDIRECT_URL = "goodfood:main"  # куда кидать после входа
LOGOUT_REDIRECT_URL = "goodfood:main"  # куда после выхода

# Это нужно, чтобы allauth не конфликтовал с кастомными шаблонами
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP-сервер и порт
EMAIL_HOST = 'smtp.gmail.com'  # для Gmail
EMAIL_PORT = 587                # TLS порт

EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'stupakviktor00@gmail.com' # ! ИЗМЕНИТЬ

# Для Gmail нужен App Password (не обычный пароль) 
EMAIL_HOST_PASSWORD = 'dsqoavnunqymugcl' #! ИЗМЕНИТЬ

# Адрес отправителя по умолчанию
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER