from .dev import *
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'hiber_test',
        'HOST': 'localhost',
        'USER': '',
    }
}
