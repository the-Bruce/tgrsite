from django.conf import settings
from django.db import models
from django.utils import encoding, safestring


class GalleryImage(models.Model):
    def __str__(self):
        return self.caption

    # Since we don't have a CDN/server for media files, we're using the gallery as static files.
    filename = models.CharField(max_length=64, blank=False)
    caption = models.CharField(max_length=1024, blank=True)

    # helper function.
    # bad practice to mix render code in with models
    # but it allows us to view images in the admin page so w/e
    @safestring.mark_safe
    def as_img(self):
        return '<img src="{}gallery_photos/{}">'.format(settings.STATIC_URL, encoding.escape_uri_path(self.filename))

    @safestring.mark_safe
    def galleryurl(self):
        return 'gallery_photos/{}'.format(encoding.escape_uri_path(self.filename))
