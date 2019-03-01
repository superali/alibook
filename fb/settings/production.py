"""
Django settings for fb project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['alibook.herokuapp.com']

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesModelBackend',
    # ...
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailAuthBackend',
]
CACHES = {
   'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
AXES_CACHE = 'axes_cache'
#AXES_ONLY_USER_FAILURES= True
AXES_COOLOFF_TIME=1
AXES_FAILURE_LIMIT=20
AXES_LOCKOUT_URL='lock'
# Application definition

INSTALLED_APPS = [
    'translations',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
   
        'rest_framework',
     'rest_framework.authtoken',

    'rest_auth'  ,
    'axes',
    'storages',
    'accounts',
    'posts',
    'pages',
    'clubs',
     'comments',
  'files',
        'actions',
        'chat',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]




ROOT_URLCONF = 'fb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'fb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



import dj_database_url
db_from_env =dj_database_url.config()
DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
LOCALE_PATHS = [
      os.path.join(BASE_DIR,'locale')
]
LANGUAGES = [
    ('en','English'),
    ('ar','Arabic'),
    ('fr','French'),
    ('de','German'),
    ('es','Spanish'),
    ('ru','Russian'),
    ('pt','Portuguese'),
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SEND_GRID_API_KEY =config('SEND_GRID_API_KEY')

DEFAULT_FROM_EMAIL = '<noreply>@alibook.herokuapp.com'

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

LOGIN_REDIRECT_URL ='/'
LOGOUT_REDIRECT_URL ='/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"alibook-storage")
]
STATIC_ROOT= os.path.join(BASE_DIR,"alibook-serve")
MEDIA_ROOT= os.path.join(BASE_DIR,"alibook-media-serve")

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
    'rest_framework.authentication.SessionAuthentication',),
    
    'DEFAULT_PERMISSION_CLASSES':(
    'rest_framework.permissions.IsAuthenticated',)
}

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME =config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
} 

AWS_LOCATION = 'static'
DEFAULT_FILE_STORAGE = 'fb.storage_backend.MediaStorage'  # <-- here is where we reference it

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'   
INTERNAL_IPS =['127.0.0.1']