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

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "production.eba-aqqrgxjn.us-west-2.elasticbeanstalk.com",
    ".elasticbeanstalk.com",  # Allows all AWS Elastic Beanstalk subdomains
]


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

WSGI_APPLICATION = "loginSignup.wsgi.application"


# Fetch S3 bucket name from AWS SSM Parameter Store
AWS_STORAGE_BUCKET_NAME = get_ssm_parameter("/django/s3_bucket_name")
AWS_S3_REGION_NAME = "your-region"  # e.g., "us-east-1"

# S3 Custom Domain
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Use S3 for Django static and media files
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Define media and static URLs
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# Configure S3 settings
AWS_QUERYSTRING_AUTH = False  # Removes authentication from URL
AWS_S3_FILE_OVERWRITE = False  # Prevents file overwriting


# Security settings
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


