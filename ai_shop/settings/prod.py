from .base import *

DEBUG = env.bool("DEBUG", default=False)

# Render runs behind a proxy, so tell Django how to detect https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# If you enable this, above header is important to avoid redirect issues
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)

# Fix common 403/CSRF issues on Render + custom domain later
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "https://*.onrender.com",
    ],
)
