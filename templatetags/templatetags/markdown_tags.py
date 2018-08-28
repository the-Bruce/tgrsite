from django import template
from markdown import markdown
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()
exts = ['markdown.extensions.nl2br', 'pymdownx.caret', 'pymdownx.tilde']

@register.filter(is_safe=True)
def parse_md(value):
	return mark_safe(markdown(escape(value), extensions=exts))

# Parses markdown WITHOUT escaping. Use with caution!
@register.filter(is_safe=True)
def parse_md_safe(value):
	return mark_safe(markdown(value, extensions=exts))
