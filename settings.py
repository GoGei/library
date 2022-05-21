import os

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__))) + '/'

SECRET_KEY = 'secret-key'

DEBUG = False
INSECURE = False
API_DOCUMENTATION = True
DEBUG_TOOLBAR = True

ALLOWED_HOSTS = ['*']

SITE_URL = 'library.local'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = None
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_hosts',
    'django_filters',
    'widget_tweaks',
    'corsheaders',
    'rest_framework',
    'drf_yasg2',
    'ckeditor',
    'ckeditor_uploader',
    'core.Utils',
    'core.User',
]

AUTH_USER_MODEL = 'User.User'

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_DOMAIN = f'.{SITE_URL}'
SESSION_COOKIE_DOMAIN = f'.{SITE_URL}'

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'urls'
DEFAULT_HOST = 'public'
ROOT_HOSTCONF = 'hosts'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + 'core/templates/',
            BASE_DIR + 'Public/templates/',
            BASE_DIR + 'Admin/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'library',
        'USER': 'library',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'htdocs')
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, 'media/ckeditoruploads/')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
    'admin': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Outdent', 'Indent',
             '-', 'Link', 'Unlink',
             'Format',
             ],
            ['HorizontalRule',
             '-', 'BulletedList', 'NumberedList',
             '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
             '-', 'SpecialChar',
             ],
            ['Maximize']
        ],
        'toolbarCanCollapse': True,
        'width': '100%',
    }
}
