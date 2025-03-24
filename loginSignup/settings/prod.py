from .base import *
import boto3
import json

DEBUG = False

# AWS SSM Parameter Store
ssm = boto3.client("ssm", region_name="your-region")

def get_ssm_parameter(name, decrypt=True):
    response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
    return response["Parameter"]["Value"]

# Fetch credentials securely from AWS SSM
SECRET_KEY = get_ssm_parameter("/django/secret_key")
ALLOWED_HOSTS = ["yourdomain.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_ssm_parameter("/django/db/name"),
        'USER': get_ssm_parameter("/django/db/user"),
        'PASSWORD': get_ssm_parameter("/django/db/password"),
        'HOST': get_ssm_parameter("/django/db/host"),
        'PORT': get_ssm_parameter("/django/db/port"),
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
