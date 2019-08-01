from .base_settings import *

DEBUG = False

AWS_STORAGE_BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME', 'leadshub-staticfiles')
AWS_S3_REGION_NAME = 'eu-west-2'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID', 'AKIAIYBOZKG7LNFWN5FA')
AWS_SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY', 'UX2iwXjKirMAQ+uDbhquu2yjZYhPFgHEpO/rKK90')

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'