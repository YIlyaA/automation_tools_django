from email.policy import default
from pathlib import Path
# from re import template
from unittest.mock import DEFAULT
from decouple import config

from django.conf.global_settings import DEFAULT_FROM_EMAIL, MEDIA_ROOT, MEDIA_URL, STATICFILES_DIRS

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)  # True or Fasle

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # crispy filters for forms
    'crispy_forms',
    'crispy_bootstrap5',

    # CKEditro for customizing emails
    'ckeditor',

    # another smpt 
    'anymail',

    'dataentry',
    'uploads',
    'emails',
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

ROOT_URLCONF = 'awd_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'awd_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / config('DATABASE_URL', default='db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'awd_main/static'
]

# Media file config
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",
    50: "critical",
}


# celery config
CELERY_BROKER_URL = 'redis://localhost:6379'


# ========================================

# email configuration 
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Automate with Django <anukovich2@gmail.com>'
DEFAULT_TO_EMAIL = 'yanukovichilya@gmail.com'

# USING ANOTHER SMTP
ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "SENDINBLUE_API_KEY": config("SENDINBLUE_API_KEY"),
}
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"  # or sendinblue.EmailBackend, or...

# ========================================


CRISPY_TEMPLATE_PACK = 'bootstrap5'


CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'full',
        'height': 200,
    },
}

CSRF_TRUSTED_ORIGINS = [
    'https://8937-109-173-214-39.ngrok-free.app'    # trust to ngrok url to login, register
]
BASE_URL='https://8937-109-173-214-39.ngrok-free.app'