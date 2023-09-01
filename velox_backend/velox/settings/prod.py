import os
import environ

from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += [
    'debug_toolbar',
]

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))
DEBUG = False

DB_USERNAME = env('DB_USERNAME')
DB_PASSWORD = env('DB_PASSWORD')
DB_NAME = env('DB_NAME')
HOSTNAME = env('HOSTNAME')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '/cloudsql/velox-horse1:us-central1:velox',
        # 'USER': 'postgres',
        # 'PASSWORD': 'vqH5N7d6sywyxDiG',
        # 'NAME': 'velox_db',
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'NAME': DB_NAME

    }
}

STATIC_URL = "/static/"

GS_BUCKET_NAME = env('GS_BUCKET_STATIC')
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"
GS_EXPIRATION = 0

# GCS_BUCKET = 'velox-biomechanics-data'
GCS_BUCKET = env('GCS_BUCKET')

ALLOWED_HOSTS = ['*']

import google.cloud.logging

client = google.cloud.logging.Client(project='velox-horse1')
client.setup_logging()

