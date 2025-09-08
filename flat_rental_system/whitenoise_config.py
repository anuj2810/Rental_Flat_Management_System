"""
Custom WhiteNoise configuration to serve media files in production.
"""
from whitenoise.middleware import WhiteNoiseMiddleware
from django.conf import settings
import os


class WhiteNoiseMediaMiddleware(WhiteNoiseMiddleware):
    """
    Custom WhiteNoise middleware that serves media files in production.
    This is needed because WhiteNoise doesn't serve media files by default.
    """

    def __init__(self, get_response):
        super().__init__(get_response)

        # Add media files to be served by WhiteNoise
        if hasattr(settings, 'MEDIA_ROOT') and hasattr(settings, 'MEDIA_URL'):
            media_root = str(settings.MEDIA_ROOT)
            media_url = settings.MEDIA_URL.rstrip('/')

            # Only add if media directory exists
            if os.path.exists(media_root):
                self.add_files(media_root, prefix=media_url)
