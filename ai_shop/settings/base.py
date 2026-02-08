# from pathlib import Path
# import environ
# import os
# import dj_database_url

# # BASE_DIR points to folder with manage.py
# BASE_DIR = Path(__file__).resolve().parent.parent.parent

# # Load .env
# env = environ.Env(DEBUG=(bool, False))
# environ.Env.read_env(BASE_DIR / ".env")

# SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-me")
# DEBUG = env.bool("DEBUG", default=True)
# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost", ".onrender.com"])


# INSTALLED_APPS = [
#     # Django default
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",

#     # Required for django-allauth
#     "django.contrib.sites",

#     # allauth core
#     "allauth",
#     "allauth.account",
#     "allauth.socialaccount",

#     # Google provider
#     "allauth.socialaccount.providers.google",

#     # Local apps
#     "accounts",
#     "shop",
#     "cart",
#     "checkout",
#     "analytics",
# ]

# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",

#     # allauth (required in recent versions)
#     "allauth.account.middleware.AccountMiddleware",

#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
#     "django.middleware.security.SecurityMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",
# ]

# ROOT_URLCONF = "ai_shop.urls"

# TEMPLATES = [{
#     "BACKEND": "django.template.backends.django.DjangoTemplates",
#     "DIRS": [BASE_DIR / "templates"],
#     "APP_DIRS": True,
#     "OPTIONS": {
#         "context_processors": [
#             "django.template.context_processors.debug",
#             "django.template.context_processors.request",  # REQUIRED for allauth
#             "django.contrib.auth.context_processors.auth",
#             "django.contrib.messages.context_processors.messages",

#             # Your existing processors
#             "shop.context_processors.category_list",
#             "cart.context_processors.cart_summary",

#             # ✅ expose Revolut.Me link to all templates
#             "checkout.context_processors.revolut_link",
#         ]
#     },
# }]

# WSGI_APPLICATION = "ai_shop.wsgi.application"

# # Database (SQLite for now; can switch to Postgres later using DATABASE_URL)
# DATABASES = {
#     "default": env.db(
#         "DATABASE_URL",
#         default=f"sqlite:///{(BASE_DIR / 'db.sqlite3').as_posix()}"
#     )
# }


# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# ]

# # Sites framework (required by allauth)
# SITE_ID = env.int("SITE_ID", default=2)

# # allauth (new settings style)
# ACCOUNT_LOGIN_METHODS = {"email"}
# ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
# ACCOUNT_EMAIL_VERIFICATION = "optional"
# ACCOUNT_SESSION_REMEMBER = True
# ACCOUNT_LOGOUT_ON_GET = False

# # Redirects
# LOGIN_REDIRECT_URL = "home"
# LOGOUT_REDIRECT_URL = "home"

# # Google provider settings
# SOCIALACCOUNT_QUERY_EMAIL = True
# SOCIALACCOUNT_LOGIN_ON_GET = True
# SOCIALACCOUNT_PROVIDERS = {
#     "google": {
#         "SCOPE": ["profile", "email"],
#         "AUTH_PARAMS": {"access_type": "online"},
#     }
# }

# # Revolut settings (Revolut.Me only in your case)
# REVOLUT_ME_LINK = env("REVOLUT_ME_LINK", default="https://revolut.me/subrah2xwv")

# # Keep these for future (merchant integration). They can stay blank safely.
# REVOLUT_MODE = env("REVOLUT_MODE", default="sandbox")
# REVOLUT_API_KEY = env("REVOLUT_API_KEY", default="")
# REVOLUT_WEBHOOK_SECRET = env("REVOLUT_WEBHOOK_SECRET", default="")
# REVOLUT_SUCCESS_URL = env("REVOLUT_SUCCESS_URL", default="http://127.0.0.1:8000/checkout/success/")
# REVOLUT_CANCEL_URL = env("REVOLUT_CANCEL_URL", default="http://127.0.0.1:8000/checkout/cancel/")

# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "Europe/Dublin"
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [BASE_DIR / "static"]

# STORAGES = {
#     "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
# }


# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
from pathlib import Path
import os
import environ

# base.py is inside: ai_shop/settings/base.py
# So project root (where manage.py is) = 3 levels up
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# .env loader
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-me")
DEBUG = env.bool("DEBUG", default=False)

# Robust ALLOWED_HOSTS (handles wrong formatting too)
default_hosts = ["127.0.0.1", "localhost", "0.0.0.0", ".onrender.com"]
raw_hosts = os.getenv("ALLOWED_HOSTS", "")
if raw_hosts.strip().startswith("[") and raw_hosts.strip().endswith("]"):
    # if user stored JSON-like list in env by mistake: ["a","b"]
    raw_hosts = raw_hosts.strip().strip("[]").replace('"', "").replace("'", "")

ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()] or default_hosts

# Render external hostname (if present)
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    # Django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # django-allauth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Local apps
    "accounts",
    "shop",
    "cart",
    "checkout",
    "analytics",
]

MIDDLEWARE = [
    # ✅ correct order (Security first, then WhiteNoise)
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # allauth
    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ai_shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # required for allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "shop.context_processors.category_list",
                "cart.context_processors.cart_summary",
                "checkout.context_processors.revolut_link",
            ]
        },
    }
]

WSGI_APPLICATION = "ai_shop.wsgi.application"

# Database: default sqlite, Render can override with DATABASE_URL
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{(BASE_DIR / 'db.sqlite3').as_posix()}"
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = env.int("SITE_ID", default=2)

# allauth modern settings
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = False

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Dublin"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
