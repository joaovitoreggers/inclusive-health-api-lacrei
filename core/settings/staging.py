# config/settings/staging.py
from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# endurecimento de segurança atrás de proxy/load balancer
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True