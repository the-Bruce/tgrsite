from django import template
from django.templatetags import static
from django.utils.html import escape
from django.utils.safestring import mark_safe
from markdown import markdown
from bleach.sanitizer import Cleaner

register = template.Library()
exts = ['markdown.extensions.nl2br', 'pymdownx.caret', 'pymdownx.tilde', 'sane_lists']


@register.filter(is_safe=True)
def parse_md(value):
    return split_escape_after(markdown(split_escape_before(value), extensions=exts, output_format='html5'))


# Parses markdown WITHOUT escaping. Use with caution!
@register.filter(is_safe=True)
def parse_md_safe(value):
    return mark_safe(markdown(value, extensions=exts, output_format='html5'))


class FullStaticNode(static.StaticNode):
    def url(self, context):
        request = context['request']
        return request.build_absolute_uri(super().url(context))


@register.tag('fullstatic')
def do_static(parser, token):
    return FullStaticNode.handle_token(parser, token)


_html_escapes_before = {
    ord('&'): '&amp;',
    ord('<'): '&lt;',
    # ord('>'): '&gt;', # Potentially risky, using bleach to help mitigate this, but allows blockquotes
}

_html_escapes_after = {
    ord('"'): '&quot;',
    ord("'"): '&#39;',
}


def split_escape_before(text):
    return str(text).translate(_html_escapes_before)


def split_escape_after(text):
    text = str(text).translate(_html_escapes_after)
    cleaner = Cleaner(tags=['p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'strong', 'a', 'ul', 'ol', 'li',
                            'blockquote', 'img', 'pre', 'code', 'hr'],
                      attributes={'a': ['href']}, protocols=['http', 'https'])
    text = cleaner.clean(text)
    return mark_safe(text)
