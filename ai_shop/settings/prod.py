from .base import *
import os

DEBUG = False

# ✅ Render runs behind a proxy (important)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ✅ This prevents common 400/CSRF issues on Render
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# If you set a custom domain, add it too:
# CSRF_TRUSTED_ORIGINS += ["https://yourdomain.com"]

# ✅ Ensure your exact Render URL is allowed (avoid DisallowedHost 400)
# Add your service host explicitly if you know it:
if "ai-shop-amazon.onrender.com" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("ai-shop-amazon.onrender.com")

# If you move to Postgres later, set DATABASE_URL in Render env and switch like this:
# import dj_database_url
# DATABASES = {
#     "default": dj_database_url.config(conn_max_age=600, ssl_require=True)
# }

# Security (optional but good)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False  # Render already handles HTTPS; keep False to avoid loops
