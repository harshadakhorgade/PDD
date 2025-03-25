from .base import *
import boto3
import os

DEBUG = False

# AWS SSM Parameter Store Setup
ssm = boto3.client("ssm", region_name="us-west-2")

def get_ssm_parameter(name, decrypt=True):
    """Fetch parameter from AWS SSM Parameter Store with fallback."""
    try:
        response = ssm.get_parameter(Name=name, WithDecryption=decrypt)
        return response["Parameter"]["Value"]
    except Exception as e:
        print(f"Warning: Could not retrieve {name} from SSM. Using fallback. Error: {e}")
        return os.getenv(name.replace("/", "_").upper(), "fallback-value")

# Set SECRET_KEY
SECRET_KEY = get_ssm_parameter("/django/secret_key") or os.getenv("SECRET_KEY", "fallback-secret-key")

# Allowed Hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,production.eba-vp5tfvub.us-west-2.elasticbeanstalk.com,.elasticbeanstalk.com").split(",")

WSGI_APPLICATION = "loginSignup.wsgi.application"

# AWS S3 Storage Configuration
AWS_STORAGE_BUCKET_NAME = get_ssm_parameter("/django/s3_bucket_name") or os.getenv("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_REGION_NAME = "us-west-2"

if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_ROOT = BASE_DIR / "media"

# Security Settings
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
