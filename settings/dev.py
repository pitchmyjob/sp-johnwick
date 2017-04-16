# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from .base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    # Thirds apps
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('DJANGO_DB_DEV_HOST'),
        'NAME': get_env_variable('DJANGO_DB_DEV_NAME'),
        'USER': get_env_variable('DJANGO_DB_DEV_USER'),
        'PASSWORD': get_env_variable('DJANGO_DB_DEV_PASSWORD'),
    }
}

REGISTER_CONFIRMATION = False