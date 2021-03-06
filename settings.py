"""
Django settings for book_rental project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# All config import
from config.settings.database import *
from config.settings.br_apps import *
from config.static_directory import *
#from config.initialize import *
from config.parameters import SUPPORTED_PRINTING_TYPES
from config.settings.hosts import BR_ALLOWED_HOSTS
import pymysql
from config.settings.email_config import *
from config.settings.google_recaptcha_config import *
from config.settings.social_login_config import *

pymysql.install_as_MySQLdb()

# End config import

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Modified Code

ENVIRONMENT = os.environ

# End Modified Code


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENVIRONMENT.get('SECRET_KEY', 'a^&%6yp#2eudk%+5v-7tkhn+hxfm2_zmm83rpp&!oe7(n@-tta')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = BR_ALLOWED_HOSTS

SITE_ID = 1
SITE_NAME = 'bookrental'

# Additional locations of static files

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'static'),
)

STATICFILES_DIRS += STATIC_FILES_DIRS

USE_I18N = True

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en_US', 'English'),
    ('zh_CN', 'Chinese'),
)

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale'),
)

# End od Language Settings

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken'
]

INSTALLED_APPS += BR_APPS

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'engine.middlewares.language_middleware.LanguageMiddleware',
    'generics.middleware.br_middleware.BRRequestMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
        ],
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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'PAGE_SIZE': 20
}

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = DATABASES_CONFIG

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

TIME_ZONE = 'UTC'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# Modification will be added here.

# google reCapatcha configurations
GOOGLE_RECAPTCHA_SITE_KEY = GOOGLE_RECAPTCHA_SITE_KEY
GOOGLE_RECAPTCHA_SECRET_KEY = GOOGLE_RECAPTCHA_SECRET_KEY

# social login configurations
FACEBOOK_APP_ID = FACEBOOK_APP_ID

CART_SESSION_ID = 'cart'
SESSION_COUPON_ID = 'coupon_code'
SESSION_COUPON_REF = 'self_coupon'
APPLY_BEST_COUPON_PROMO = False
USER_LOGIN_URL = "/auth/login/"
ADMIN_LOGIN_URL = "/admin/login/"

# after 7 days password reset link will disable automatically
PASSWORD_RESET_TIMEOUT_DAYS = 7

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MEDIA_TEMP_PATH = os.path.join(MEDIA_ROOT,"temp")
MEDIA_AUTHOR_PATH = os.path.join(MEDIA_ROOT,"author")
MEDIA_PUBLISHER_PATH = os.path.join(MEDIA_ROOT,"publisher")
MEDIA_BOOK_PATH = os.path.join(MEDIA_ROOT,"books")
MEDIA_AUTHOR_THUMB_PATH = os.path.join(MEDIA_AUTHOR_PATH,"thumbnails")
MEDIA_PUBLISHER_THUMB_PATH = os.path.join(MEDIA_PUBLISHER_PATH,"thumbnails")
MEDIA_BOOK_THUMB_PATH = os.path.join(MEDIA_BOOK_PATH,"thumbnails")


GLOBAL_MODEL_FILTER = {"is_deleted":False}

DEFAULT_FALLBACK_TZ = "Asia/Dhaka"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
