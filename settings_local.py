# Consider ourself as internal IP
from socket import gethostname, gethostbyname
INTERNAL_IPS = ( '127.0.0.1', 
                 gethostbyname(gethostname()),)

DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS' : False }

# Make this unique, and don't share it with anybody.
SECRET_KEY = '__0(6(#-mf*928p9n7_xhcn09yxshtuf1y5b75zizisar#0@jh'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'nl-nl'

#DATABASE_ENGINE = 'mysql'
#DATABASE_NAME = ''
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

#DEBUG = False

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.request")


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django_extensions',
    'debug_toolbar',
    'representations',
    'typogrify',
    'metadata',
    'metaphore',
)
