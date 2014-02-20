"""
Django settings for digiapproval_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ds7pwiyk6d62xpc98ij5$4$r@!21a*5y#cf8#f3b%%xy*ibkx+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'digiapproval_project.apps.digiapproval',
    'digiapproval_project.apps.spec_builder',
    'south',
    'bootstrap3',
    'registration',
    'breadcrumbs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
    'breadcrumbs.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'digiapproval_project.urls'

WSGI_APPLICATION = 'digiapproval_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Canberra'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Fixtures
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)


# Files
DEFAULT_FILE_STORAGE = 'swift.storage.SwiftStorage'

# Bootstrap
BOOTSTRAP3 = {
    'base_url': '/static/bootstrap/dist/'
}

# Registration
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window

# breadcrumbs, acting as
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'digiapproval_project.apps.digiapproval.acting_as_processor.acting_as',
)

# Patch in our local settings
from .local_settings import *  # noqa
INSTALLED_APPS += ADDITIONAL_APPS
