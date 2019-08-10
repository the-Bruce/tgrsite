from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=25, help_text="Enter a name to help recognise it.")
    assetFile = models.FileField(upload_to='assets/%Y/%m/%d/')

    def __str__(self):
        return self.name + ': '+self.assetFile.url

# Delete the stored file when model is deleted
@receiver(post_delete, sender=Asset)
def submission_delete(sender, instance, **kwargs):
    instance.assetFile.delete(False)