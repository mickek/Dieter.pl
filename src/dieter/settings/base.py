from defaults import *

MANAGERS = ADMINS = (
    ('mklujszo', 'mklujszo@gmail.com'),
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'op56pokf54./&^%$GDAWLEosh"AP#O$%^&KLUYHBLAKLPLPkso'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    
    'dieter.home.context_processors.tabs'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'django.contrib.humanize',
    
    'south',        
    
    'dieter.dashboard',
    'dieter.diet',    
    'dieter.home',
    'dieter.patients',
    'dieter.registration',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",                           
    "dieter.auth.EmailBackend",
)

DEFAULT_FROM_EMAIL = 'kontakt@dieter.pl'
SERVER_EMAIL = 'kontakt@dieter.pl'      # E-mail address that error messages come from.

INTERNAL_IPS = ['127.0.0.1']

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

ACCOUNT_ACTIVATION_DAYS = 3

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

LOGIN_REDIRECT_URL = "/logged_in"

AUTH_PROFILE_MODULE = 'patients.profile'
