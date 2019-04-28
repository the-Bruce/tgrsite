from django import template

from website_settings import models

register = template.Library()


@register.simple_tag
def string_setting(key):
    try:
        res = models.StringProperty.objects.get(key__iexact=key).value
    except models.StringProperty.DoesNotExist:
        res = ""
    return res
