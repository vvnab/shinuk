# Django settings for shinuk project.

from os.path import join, dirname
PROJECT_ROOT = dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('vvnab', 'vvnab@ya.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'shinuk',                      # Or path to database file if using sqlite3.
#        'NAME': 'shinuk2',                      # Or path to database file if using sqlite3.
        'USER': 'shinuk',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+_^ehvr%86-hkup(^1nwdsmga%n@j=fltid4#t08#2s4d+86q9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'shinuk.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.webdesign',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.flatpages',
#    'django.contrib.comments',
    'goods',
    'accounts',
    'orders',
#    'robokassa',
    'ecommerce',
#    'django_qiwi',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS, DATE_FORMAT, DATETIME_FORMAT

SESSION_COOKIE_AGE = 60 * 60 * 24 * 90

TEMPLATE_CONTEXT_PROCESSORS += 'context_processors.context',
DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y : P'
AUTH_PROFILE_MODULE = 'accounts.Profile'

CACHE_BACKEND = 'locmem:///'

#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
ROBOKASSA_LOGIN = 'vvnab'
ROBOKASSA_PASSWORD1 = '6a3Uj95Oksd42'
ROBOKASSA_PASSWORD2 = '78GerSpld8a7S'
ROBOKASSA_TEST_MODE = True

#E-COMMERCE
GATEWAY_URL = 'https://3ds.mmbank.ru:443/cgi-bin/cgi_link'
CURRENCY = 'RUR'
MERCH_NAME = 'Shinuk LTD'
MERCH_URL = 'www.shinuk.ru'
MERCHANT = '465206022687101'
TERMINAL = '22687101'
EMAIL = 'admin@shinuk.ru'
COUNTRY = 'RU'
MERCH_GMT = ''
BACKREF = 'http://shinuk.ru/accounts/profile/'
KEY =  '04A4B0E6E85BBCF8CB3FB172354CD5E6'

#QIWI
QIWI_APP = 'qiwi'
QIWI_LOGIN = '14671'
QIWI_PASSWORD = 'KT3li6LCTV'
QIWI_SOAP_SERVER = ('0.0.0.0', 17555)

# i was here

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_ROOT, 'log.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'logger': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'vvnab76@gmail.com'
EMAIL_HOST_PASSWORD = 'c156reHO'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'html'
