from django.shortcuts import reverse
from django.db import models
from django.utils import encoding, safestring

from django.db.models.signals import post_delete
from django.dispatch import receiver


class GalleryImage(models.Model):
    def __str__(self):
        return self.caption

    image = models.ImageField(upload_to='gallery/%Y/%m/%d/', blank=False)
    caption = models.CharField(max_length=1024, blank=True)

    # helper function.
    # bad practice to mix render code in with models
    # but it allows us to view images in the admin page so w/e
    @safestring.mark_safe
    def as_img(self):
        return '<img src="{}" width=400>'.format(encoding.escape_uri_path(self.image.url))

    def get_absolute_url(self):
        return reverse("gallery:gallery")


# Delete the stored file when model is deleted
@receiver(post_delete, sender=GalleryImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
