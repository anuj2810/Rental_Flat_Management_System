"""
Custom storage backends for handling media files in production.
This ensures uploaded files persist across deployments.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """Custom storage for media files using AWS S3 or compatible services"""
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False


class StaticStorage(S3Boto3Storage):
    """Custom storage for static files using AWS S3 or compatible services"""
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    custom_domain = False
