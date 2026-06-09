from .staging import *  
from .base import *  # noqa


SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


LOGGING["formatters"]["json"] = {
    "()": "pythonjsonlogger.json.JsonFormatter",   # caminho do v3+; o "jsonlogger" antigo está deprecado
    "format": "%(levelname)s %(asctime)s %(name)s %(module)s %(lineno)d %(message)s",
}
LOGGING["handlers"]["console"]["formatter"] = "json"