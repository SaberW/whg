"""
Generated by 'django-admin startproject' using Django 2.0.7.

update to 2.1.2 13 Oct 2018

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'saiz(s6w1+okoz@3duv!%3bv=4cei8--f+5jb=a*_3&l0u!!wr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    
    'django_celery_beat',
    'django_celery_results',
    'leaflet',
    'djgeojson',
    'fontawesome',
    'mathfilters',
    'rest_framework',

    'accounts.apps.AccountsConfig',
    'areas.apps.AreasConfig',
    'datasets.apps.DatasetsConfig',
    'main.apps.MainConfig',
    'maps.apps.MapsConfig',
    'search.apps.SearchConfig',
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

ROOT_URLCONF = 'whg.urls'

TIME_ZONE = 'America/New_York'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'main/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'builtins': [
                'whg.builtins',
            ]
        },
    },
]

WSGI_APPLICATION = 'whg.wsgi.application'

LEAFLET_CONFIG = {
    'TILES':'https://api.mapbox.com/v4/mapbox.light/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia2dlb2dyYXBoZXIiLCJhIjoiY2prcmgwc2cwMjRuZzNsdGhzZmVuMDRqbCJ9.MeLsyeOqwhTRdvt_Hgo7kg',
    'DEFAULT_CENTER': (40.0, 15.0),
    'DEFAULT_ZOOM': 1,
    'MIN_ZOOM': 1,
    'MAX_ZOOM': 18,
    'RESET_VIEW': False,
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # authentication, etc.
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'whg',
        'USER':'',
        'PASSWORD':'',
        'HOST':'localhost',
        'PORT':'5432',
    },
    # not implemented
    # 'whgdata': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'whgdata',
    #     'USER':'',
    #     'PASSWORD':'',
    #     'HOST':'localhost',
    #     'PORT':'5432',
    # }
}

# not implemented
# DATABASE_ROUTERS = ('whg.dbrouters.MyDBRouter',)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'whg/static/'),
    os.path.join(BASE_DIR, 'datasets/static/'),
]

try:
    from local_settings import *
except ImportError:
    pass
