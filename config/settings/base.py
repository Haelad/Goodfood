from pathlib import Path

from decouple import config

SECRET_KEY = config("SECRET_KEY")

# ----------------------------
# Пути
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# ----------------------------
# Приложения
# ----------------------------
INSTALLED_APPS = [
    # Приложения проекта
    "apps.users",
    "apps.goodfood",
    # Unfold
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    "unfold.contrib.constance",
    "unfold.contrib.hijack",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.postgres",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Безопасность
    "csp",
    # Аутентификация
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # UI
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
]

# ----------------------------
# Middleware
# ----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------
# Шаблоны
# ----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

# ----------------------------
# Auth / Allauth
# ----------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_LOGIN_METHODS = {"email", "username"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]

ACCOUNT_FORMS = {
    "login": "apps.users.forms.CustomLoginForm",
    "signup": "apps.users.forms.CustomSignupForm",
}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "goodfood:main"
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"

LOGIN_REDIRECT_URL = "goodfood:main"
LOGOUT_REDIRECT_URL = "goodfood:main"

# ----------------------------
# Валидация паролей
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------
# Дата и время
# ----------------------------
DATETIME_INPUT_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %I:%M %p",
    "%d-%b-%Y %H:%M:%S",
)
USE_TZ = True
YEAR_MONTH_FORMAT = "m/Y"

# ----------------------------
# Статика и медиа (директории)
# STATIC_ROOT переопределяется в prod
# ----------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------
# Default auto field
# ----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


UNFOLD = {
    "SITE_TITLE": "Goodfood",
    "SITE_HEADER": "Goodfood Admin",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "BORDER_RADIUS": "12px",
    "COLORS": {
        "base": {
            "50": "#f0f0f5",
            "100": "#e2e2ec",
            "200": "#c9c9d9",
            "300": "#a8a8bf",
            "400": "#7d7d99",
            "500": "#5c5c78",
            "600": "#46465e",
            "700": "#33334a",
            "800": "#221f38",  # ~ --color-main-bg
            "900": "#141223",  # ~ --color-bg-nav
            "950": "#050610",  # ~ --color-bg
        },
        "primary": {
            "50": "#f4f8e9",
            "100": "#ECF39E",  # --color-lime
            "200": "#d3e6a8",
            "300": "#b8d97a",
            "400": "#90A955",  # --color-palm
            "500": "#4F772D",  # --color-fern (основной акцент)
            "600": "#3f6224",
            "700": "#31572C",  # --color-hunter
            "800": "#1f3d1f",
            "900": "#132A13",  # --color-evergreen
            "950": "#0a1a0a",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "rgba(255, 255, 255, 0.55)",  # --color-text-muted
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "#ffffff",  # --color-text
        },
    },
    # "SIDEBAR": {
    #     "show_search": True,
    #     "show_all_applications": False,
    #     "navigation": [
    #         {
    #             "title": _("Управление"),
    #             "separator": True,
    #             "collapsible": True,
    #             "items": [
    #                 {
    #                     "title": _("Dashboard"),
    #                     "icon": "dashboard",
    #                     "link": reverse_lazy("admin:main"),
    #                 },
    #                 {
    #                     "title": _("Категории"),
    #                     "icon": "category",
    #                     "link": reverse_lazy("admin:_category"),
    #                 },
    #                 {
    #                     "title": _("Товары"),
    #                     "icon": "inventory_2",
    #                     "link": reverse_lazy("admin:goodfood_product_changelist"),
    #                 },
    #             ],
    #         },
    #     ],
    # },
}
