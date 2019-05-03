from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=cq64)k5m39kcf0lq@q_^$s1xj@hasgh!fgoe4g_y@8&0y2hck'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS.append('django_extensions')

CORS_ORIGIN_REGEX_WHITELIST = [
    r'^(http)(s)?(://192.168.1.)([0-9])([0-9])?([0-9])?',
    r'^(http)(s)?(://localhost:808)([0-9])',
    r'^(http)(s)?(://127.0.0.1:808)([0-9])'
]

try:
    from .local import *
except ImportError:
    pass
