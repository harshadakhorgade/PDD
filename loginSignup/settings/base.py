from pathlib import Path
import os
import boto3

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize AWS SSM client
ssm = boto3.client("ssm", region_name="us-west-2")

# Function to get parameters from AWS SSM
def get_ssm_parameter(name, decrypt=True):
    """Fetch parameter from AWS SSM Parameter Store."""
    try:
        response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
        return response["Parameter"]["Value"]
    except Exception as e:
        print(f"Warning: Could not retrieve {name} from SSM. Using fallback. Error: {e}")
        return os.getenv("SECRET_KEY", "fallback-secret-key")

# Fetch SECRET_KEY
SECRET_KEY = get_ssm_parameter("/django/secret_key")

# Allowed Hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "yourdomain.com,.elasticbeanstalk.com").split(",")

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'base',
    'storages',
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

ROOT_URLCONF = 'loginSignup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'loginSignup.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media Files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Authentication
LOGIN_REDIRECT_URL = 'base:home'
LOGOUT_REDIRECT_URL = 'base:login'

# REST Framework Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
