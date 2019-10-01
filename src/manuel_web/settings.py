"""
Django settings for manuel_web project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1q%zz*1==q9f8qizynbncke8mci*&vw07024f5qzz1iyee8_2c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['104.248.12.122']

LOGIN_URL = 'accounts:login'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_mysql',
    'accounts.apps.AccountsConfig',
    'patios.apps.PatiosConfig',
]

AUTH_USER_MODEL = 'accounts.Usuario'


SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'manuel_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'manuel_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE' : 'django.db.backends.mysql',
#             'USER' : 'root',
#             'PASSWORD':'2015065',
#             'NAME' : 'manuel_web',
#             'HOST':'localhost',
#             'PORT' : '3306',
#             'OPTIONS': {
#                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#                 # Tell MySQLdb to connect with 'utf8mb4' character set
#                 'charset': 'utf8mb4',
#             },
#             # Tell Django to build the test database with the 'utf8mb4' character set
#             'TEST': {
#                 'CHARSET': 'utf8mb4',
#                 'COLLATION': 'utf8mb4_unicode_ci',
#             }
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'USER' : 'niovan',
        'PASSWORD':'2015065',
        'NAME' : 'manuel_web',
        'HOST':'localhost',
        'PORT' : '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            # Tell MySQLdb to connect with 'utf8mb4' character set
            'charset': 'utf8mb4',
        },
        # Tell Django to build the test database with the 'utf8mb4' character set
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-pr'

TIME_ZONE = 'America/Puerto_Rico'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

LOCAL_STATIC_CDN_PATH = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')

STATIC_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, 'static') # live cdn AWS S3
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_cdn')
]

MEDIA_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, 'media')
MEDIA_URL = '/media/'


EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = '2525'
EMAIL_HOST_USER = 'b4a2c65fbc0669'
EMAIL_HOST_PASSWORD = '245e065f8eba19'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False