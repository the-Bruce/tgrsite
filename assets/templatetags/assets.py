from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def visual_asset(context, asset):
    return asset.url(context['request'])
