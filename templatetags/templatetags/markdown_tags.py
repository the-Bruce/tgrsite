from django import template
from markdown import markdown
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

@register.filter(is_safe=True)
def parse_md(value):
	return mark_safe(markdown(escape(value), extensions=['markdown.extensions.nl2br']))

# Parses markdown WITHOUT escaping. Use with caution!
@register.filter(is_safe=True)
def parse_md_safe(value):
	return mark_safe(markdown(value, extensions=['markdown.extensions.nl2br']))
