"""
Django settings for tradeworld project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

PROJECT_FOLDER = os.getcwd()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j0fyf510lvqlmj&4fhhhcl=9=(c3f6_&n3pt0h!sso6f4@h5k#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_accounts',
    'homepage',
    'about_us',
    'contact_us',
    'packages',
    'pricing',
    'articleApp',
    'dashboard',
    'tender_loader',
    'tender_matching_engine',
    'tender_details',
    'ckeditor',
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
    'tenderwiz.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'tenderwiz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['tenderwiz/templates'],
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

WSGI_APPLICATION = 'tenderwiz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tenderwiz_db',
        'USER': 'postgres',
        'PASSWORD': 'ayaman',
        'HOST': '',
        'PORT': '',
    }
}

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500


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


LOGIN_EXEMPT_URLS = (
    r'^$',
    r'^tenders/',
    r'^pricing/',
    r'^articles/',
    r'^contact_us/',
    r'^user_accounts/logout_success/$',
    r'^user_accounts/register/$',
    r'^user_accounts/auth/$',
    r'^user_accounts/password_reset/$',
    r'^user_accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    r'^user_accounts/register/(?P<billing_cycle>\d)/(?P<pk>\d+)/$',
    r'^user_accounts/password_reset/done/$',
    r'^user_accounts/reset/done/$',
    r'^user_accounts/auto_complete_search/$',
    r'^user_accounts/registration_success/$',
    r'^user_accounts/payment_success/$',
    r'^user_accounts/payment_cancelled/$',
    r'^user_accounts/invoice/(?P<user_id>\d+)/(?P<comp_prof_id>\d+)/$',
    r'^province/(?P<province_pk>\d+)/$',
    r'^privacy_policy/$',
    r'^termsAndConditions/$',
    r'^about_us/$',
)


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, '../static'),)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/Media')

LOGIN_REDIRECT_URL = '/user_accounts/dashboard/'
LOGIN_URL = '/user_accounts/login/'


GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'Leads Hub <tenders@leadshub.co.za>'


import django_heroku
# TEST_RUNNER = 'django_heroku.HerokuDiscoverRunner'
#
#
# AWS_STORAGE_BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME', 'leadshub-staticfiles')
# AWS_S3_REGION_NAME = 'eu-west-2'  # e.g. us-east-2
# AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID', 'AKIAIYBOZKG7LNFWN5FA')
# AWS_SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY', 'UX2iwXjKirMAQ+uDbhquu2yjZYhPFgHEpO/rKK90')
#
# # Tell django-storages the domain to use to refer to static files.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#
# # Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# # you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
