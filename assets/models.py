from django.db import models


# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length=25, help_text="Enter a name to help recognise it.")
    assetFile = models.FileField(upload_to='assets/%Y/%m/%d/')

    def __str__(self):
        return self.name + ': '+self.assetFile.url
