from pathlib import Path

import django_heroku
from dotenv import load_dotenv
from os import getenv

import cloudinary.api
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# loads the configs from .env
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'main.UserModel'
LOGIN_REDIRECT_URL = '/djangogramm/auth/login-redirect/'
LOGOUT_REDIRECT_URL = '/djangogramm/auth/login/'

# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'cloudinary',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'DjangoGramm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoGramm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DjangoGramm',
        'USER': str(getenv('USER_DB')),
        'PASSWORD': str(getenv('PASSWORD_DB')),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
django_heroku.settings(locals())

# Cloudinary
cloudinary.config(
  cloud_name=getenv('CLOUD_NAME'),
  api_key=getenv('API_KEY'),
  api_secret=getenv('API_SECRET'),
  secure=True
)

CLOUDINARY_AVATAR_FOLDER = 'avatars'
CLOUDINARY_DEFAULT_IMG = 'https://res.cloudinary.com/dbwofa3rl/image/upload/v1663590111/avatars/avatar_ox54lh.png'
CLOUDINARY_MEDIA_FOLDER = 'posts_media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = str(getenv('EMAIL'))
EMAIL_HOST_PASSWORD = str(getenv('PASSWORD_EMAIL'))
EMAIL_PORT = 587

# MEDIA
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# INTERNAL_IPS
INTERNAL_IPS = [
    "127.0.0.1",
]

# Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# GOOGLE social settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'))

# GITHUB social settings
SOCIAL_AUTH_GITHUB_KEY = str(getenv('SOCIAL_AUTH_GITHUB_KEY'))
SOCIAL_AUTH_GITHUB_SECRET = str(getenv('SOCIAL_AUTH_GITHUB_SECRET'))

# SOCIAL NAMESPACE
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Database social settings
SOCIAL_AUTH_JSONFIELD_ENABLED = True
