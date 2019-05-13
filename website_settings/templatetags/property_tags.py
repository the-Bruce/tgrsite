from django import template
from django.utils.safestring import mark_safe

from website_settings import models

register = template.Library()


@register.simple_tag
def string_setting(key):
    try:
        res = models.StringProperty.objects.get(key__iexact=key).value
    except models.StringProperty.DoesNotExist:
        res = ""
    return mark_safe(res)


@register.simple_tag
def text_setting(key):
    try:
        res = models.TextProperty.objects.get(key__iexact=key).value
    except models.TextProperty.DoesNotExist:
        res = ""
    return mark_safe(res)
