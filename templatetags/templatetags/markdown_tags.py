from django import template
from markdown import markdown
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

@register.filter(is_safe=True)
def parse_md(value):
	return mark_safe(markdown(escape(value)))
