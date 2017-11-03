from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    #Own apps
    'apps.worker.apps.WorkerConfig',
]
