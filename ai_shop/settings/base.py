from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # folder that contains manage.py

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes", "y")

# Comma-separated allowed hosts in env OR fallback
# Example env: ALLOWED_HOSTS=127.0.0.1,localhost,ai-shop-amazon.onrender.com,.onrender.com
raw_hosts = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost,.onrender.com")
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

# Render gives this automatically sometimes – add it if present
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

INSTALLED_APPS = [
    # Django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # allauth
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
    "django.middleware.security.SecurityMiddleware",

    # ✅ whitenoise must be right after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # ✅ required by recent allauth
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
                "django.template.context_processors.request",  # REQUIRED for allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "shop.context_processors.category_list",
                "cart.context_processors.cart_summary",
                "checkout.context_processors.revolut_link",
            ],
        },
    }
]

WSGI_APPLICATION = "ai_shop.wsgi.application"

# Default DB (override in prod.py if needed)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
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

SITE_ID = int(os.getenv("SITE_ID", "2"))

# allauth config (new style)
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
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Dublin")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Revolut
REVOLUT_ME_LINK = os.getenv("REVOLUT_ME_LINK", "https://revolut.me/subrah2xwv")
