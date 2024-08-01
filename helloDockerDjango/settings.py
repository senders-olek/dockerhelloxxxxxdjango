"""
Django settings for helloDockerDjango project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

from app.utils import ObfuscatedSecret
import dotenv
dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@b_yw6lg^0$7z(e43@z=e0!fs8r_5-=u=nvs_-5z1d%4g$dycm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'elasticapm.contrib.django'
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

ROOT_URLCONF = 'helloDockerDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'helloDockerDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ENV_VAR_NAMES = ['SAMPLE_ENV', 'ELASTIC_BASE_URL', 'ELASTIC_APM_SECRET_TOKEN']

SAMPLE_ENV = ObfuscatedSecret(os.getenv('SAMPLE_ENV', None))
ELASTIC_BASE_URL = ObfuscatedSecret(os.getenv('ELASTIC_BASE_URL', None))
# ELASTIC_USER = ObfuscatedSecret(os.getenv('ELASTIC_USER', None))
# ELASTIC_PASS = ObfuscatedSecret(os.getenv('ELASTIC_PASS', None))
ELASTIC_APM_SECRET_TOKEN = ObfuscatedSecret(os.getenv('ELASTIC_APM_SECRET_TOKEN', None))

ELASTIC_APM = {
    'SERVICE_NAME': 'Django-Service',
    'SERVER_URL': os.getenv('ELASTIC_BASE_URL', None),
    'ELASTIC_APM_SECRET_TOKEN': os.getenv('ELASTIC_APM_SECRET_TOKEN', None),
    # 'USERNAME': os.getenv('ELASTIC_USER', None),
    # 'PASSWORD': os.getenv('ELASTIC_PASS', None),
    # 'VERIFY_SERVER_CERT': False,  # Set to True in production with proper SSL setup
}


for env_name in ENV_VAR_NAMES:
    try:
        if env_name in os.environ:
            del os.environ[env_name]
            print(f"Deleted environment variable: {env_name}")
    except KeyError:
        print(f"Environment variable {env_name} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting {env_name}")
