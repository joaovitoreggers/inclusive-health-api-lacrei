# config/settings/production.py
from .staging import *  # noqa  (produção = staging + HSTS mais agressivo)

SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True