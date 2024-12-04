"""
Django settings for cinefile project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import dj_database_url

from pathlib import Path

DEPLOY_LOCATION = os.getenv("DEPLOY_LOCATION", "localhost")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if DEPLOY_LOCATION == "heroku":
    SECRET_KEY = os.getenv("SECRET_KEY")
else:
    SECRET_KEY = 'django-insecure-6(=-khoq_d#dsi-z&gmsr(-779sf*nh74o+a^=mzwt=$ixnte8'

# SECURITY WARNING: don't run with debug turned on in production!
if DEPLOY_LOCATION == "heroku":
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = [".herokuapp.com",
                 ".cinefile.me",
                 "localhost",
                 "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'accounts',
    'journal',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinefile.urls'

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

WSGI_APPLICATION = 'cinefile.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEPLOY_LOCATION == "heroku":
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'accounts.JUser'

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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# for media files (user uploaded files)
if DEPLOY_LOCATION == "heroku":
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
        }
    }
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    MEDIA_ROOT = "/media/"
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"
else:
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
        }
    }
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # path to the media directory
    MEDIA_URL = '/media/'  # URL prefix for serving media files

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# for secure deployment
if DEPLOY_LOCATION == "heroku":
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/journal'

TMDB_AUTH = os.getenv("TMDB_AUTH")
# load locally with
# export $(cat .env | xargs)

# configure Logging
# LOGGING = {
#     "version": 1,  # the dictConfig format version
#     "disable_existing_loggers": False,  # retain the default loggers
#     "handlers": {
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": "general.log",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",
#         },
#         "accounts": {
#             "handlers": ["file"],
#             "level": "DEBUG",
#         },
#         "journal": {
#             "handlers": ["file"],
#             "level": "DEBUG",
#         },
#     },
# }