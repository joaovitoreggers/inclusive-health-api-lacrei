# config/settings/staging.py
from .base import * 

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True