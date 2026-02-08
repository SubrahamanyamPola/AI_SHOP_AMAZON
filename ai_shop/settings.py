from pathlib import Path
import environ
import os

# -----------------------------
# BASE DIR
# -----------------------------
# This assumes:
#   project_root/
#     manage.py
#     ai_shop/
#       settings/
#         base.py  (or settings.py)
#
# If your manage.py is one level above ai_shop folder, use parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # keep as you wanted

# -----------------------------
# ENV
# -----------------------------
env = environ.Env(
    DEBUG=(bool, False),
)

# Read .env if present (local). On Render env vars are injected automatically.
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-me")
DEBUG = env.bool("DEBUG", default=False)

# Render host handling
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["127.0.0.1", "localhost", ".onrender.com"]
)

# If you set RENDER_EXTERNAL_HOSTNAME on Render (recommended)
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    if RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF trusted origins (important for POST forms + admin login)
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "https://*.onrender.com",
    ]
)

# If you want to force your specific domain:
if RENDER_EXTERNAL_HOSTNAME:
    origin = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

# Render runs behind proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# -----------------------------
# APPS
# -----------------------------
INSTALLED_APPS = [
    # Django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Sites (required for allauth)
    "django.contrib.sites",

    # allauth
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

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # ✅ WhiteNoise MUST be right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # allauth middleware (required in new versions)
    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ai_shop.urls"

# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # REQUIRED for allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "shop.context_processors.category_list",
                "cart.context_processors.cart_summary",

                # Revolut link in templates
                "checkout.context_processors.revolut_link",
            ],
        },
    }
]

WSGI_APPLICATION = "ai_shop.wsgi.application"

# -----------------------------
# DATABASE
# -----------------------------
# Uses DATABASE_URL if provided, else sqlite
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{(BASE_DIR / 'db.sqlite3').as_posix()}"
    )
}

# If you're using Postgres on Render, add in Render:
# DATABASE_URL=postgres://....

# -----------------------------
# AUTH / ALLAUTH
# -----------------------------
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

SITE_ID = env.int("SITE_ID", default=1)

# allauth settings (works with modern allauth versions)
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

# -----------------------------
# REVOLUT
# -----------------------------
REVOLUT_ME_LINK = env("REVOLUT_ME_LINK", default="https://revolut.me/subrah2xwv")
REVOLUT_MODE = env("REVOLUT_MODE", default="sandbox")
REVOLUT_API_KEY = env("REVOLUT_API_KEY", default="")
REVOLUT_WEBHOOK_SECRET = env("REVOLUT_WEBHOOK_SECRET", default="")
REVOLUT_SUCCESS_URL = env("REVOLUT_SUCCESS_URL", default="http://127.0.0.1:8000/checkout/success/")
REVOLUT_CANCEL_URL = env("REVOLUT_CANCEL_URL", default="http://127.0.0.1:8000/checkout/cancel/")

# -----------------------------
# I18N
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Dublin"
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC / MEDIA
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise storage (manifest)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
