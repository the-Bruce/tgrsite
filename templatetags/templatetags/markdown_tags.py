from django import template
from django.templatetags import static
from django.utils.html import escape
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()
exts = ['markdown.extensions.nl2br', 'pymdownx.caret', 'pymdownx.tilde']


@register.filter(is_safe=True)
def parse_md(value):
    return mark_safe(markdown(escape(value), extensions=exts))


# Parses markdown WITHOUT escaping. Use with caution!
@register.filter(is_safe=True)
def parse_md_safe(value):
    return mark_safe(markdown(value, extensions=exts))


class FullStaticNode(static.StaticNode):
    def url(self, context):
        request = context['request']
        return request.build_absolute_uri(super().url(context))


@register.tag('fullstatic')
def do_static(parser, token):
    return FullStaticNode.handle_token(parser, token)
