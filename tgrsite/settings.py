"""
Django settings for tgrsite project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TODO: Once the mail server is set up change this to be the internal webmonkey address
ADMINS=  [('Webadmin', 'ashbc@users.noreply.github.com')]
MANAGERS=[('Webadmin', 'ashbc@users.noreply.github.com')]
LOGIN_URL='/login/'

s = ''
try:
    from .keys import secret
    s = secret()
except ModuleNotFoundError:
    # this will throw a KeyError and crash if neither are specified.
    # good.
    s = os.environ['SECRET_KEY']
SECRET_KEY = s


DEBUG = True

ALLOWED_HOSTS = ['aesc.pythonanywhere.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'forum.apps.ForumConfig',
    'users.apps.UsersConfig',
    'rpgs.apps.RpgsConfig',
    'statics.apps.StaticsConfig',
    'exec.apps.ExecConfig',
    'templatetags.apps.TemplatetagsConfig',
    'messaging.apps.MessagingConfig',
    'bugreports.apps.BugreportsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tgrsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tgrsite/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tgrsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# TODO: remove sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# site URL that static files are served from
STATIC_URL = '/static/'
# directories to collect static files from
STATICFILES_DIRS = (
    # this is where all our actual static files are gonna be put.
    os.path.join(BASE_DIR, 'static_resources'),
 )
# the folder to store the static files...
# where to put these such that it has permission to write there?
# in place? for now haha
# in order to serve these we need to wsgi a server
STATIC_ROOT=os.path.join(BASE_DIR, 'STATIC')

# Monday
FIRST_DAY_OF_WEEK=1

# as advised by python manage.py check --deploy
# prevent browsers from MIME type sniffing. doesn't play nice
# SECURE_CONTENT_TYPE_NOSNIFF=True

# enable browsers' XSS filters
SECURE_BROWSER_XSS_FILTER=True

# ensure all traffic is SSL (https)
# SECURE_SSL_REDIRECT=True
# session cookies secure-only
# SESSION_COOKIE_SECURE=True
# same for CSRF cookie
# CSRF_COOKIE_SECURE=True
# CSRF_COOKIE_HTTPONLY=True
X_FRAME_OPTIONS='DENY'
