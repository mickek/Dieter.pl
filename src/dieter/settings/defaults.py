import os
from django.conf import ENVIRONMENT_VARIABLE

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = False

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DJANGO_PATH = os.path.join(ROOT_PATH, os.path.join(ROOT_PATH, 'libs', 'django'))
PROJECT_NAME = os.path.basename(ROOT_PATH)
SETTINGS_NAME = os.environ[ENVIRONMENT_VARIABLE].split(".")[-1]

DATABASE_ENGINE = 'postgresql_psycopg2'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = PROJECT_NAME + "_" + SETTINGS_NAME    # Or path to database file if using sqlite3.
DATABASE_USER = 'postgres'                      # Not used with sqlite3.
DATABASE_PASSWORD = ''                          # Not used with sqlite3.
DATABASE_HOST = ''                              # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                              # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl-pl'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

ROOT_URLCONF = PROJECT_NAME + '.urls'

MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/s/'

DYNAMIC_MEDIA = 'd/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

AWS_STORAGE_BUCKET_NAME = PROJECT_NAME + "_" + SETTINGS_NAME
AWS_SDB_DOMAIN = PROJECT_NAME + "_" + SETTINGS_NAME

try:
    os.makedirs(os.path.join(MEDIA_ROOT, DYNAMIC_MEDIA))
except Exception:
    pass