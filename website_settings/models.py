from django.db import models

"""
    Note: I know this is a sub-optimal way of achieving what it achieves. 
    I know that doing this properly would help the site in the future.
    However, this solves the problem in a far better way than the current solution
    (editing templates when stuff changes) and is far less disruptive than rewriting the current system into a
    more traditionally engineered solution (for which a large amount of the current infrastructure would need to be
    discarded.)
    
    Future webdevs: please excuse this act, or at least view it in the context it was conceived within.
    And may god have mercy upon my soul.
"""


# Create your models here.
class StringProperty(models.Model):
    key = models.CharField(max_length=25)
    value = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "String Properties"

    def __str__(self):
        return self.key


class TextProperty(models.Model):
    key = models.CharField(max_length=25)
    value = models.TextField()

    class Meta:
        verbose_name_plural = "Text Properties"

    def __str__(self):
        return self.key
