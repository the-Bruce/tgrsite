from django.db import models


# Create your models here.
class Redirect(models.Model):
    source = models.CharField(max_length=30)
    sink = models.CharField(max_length=250)
    permanent = models.BooleanField(default=False)

    def __str__(self):
        return self.source
