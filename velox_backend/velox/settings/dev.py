import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)

from .base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += ['debug_toolbar',]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1', ]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'NAME': 'velox_db_dev',
    }
}


GS_BUCKET_NAME = "velox_webapp_static"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"
GS_EXPIRATION = 0
STATIC_URL = "/static/"

GCS_BUCKET = 'velox-biomechanics-dev'
