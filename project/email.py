from settings import *
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
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