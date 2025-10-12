from settings import *

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








