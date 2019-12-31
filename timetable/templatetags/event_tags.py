from django import template
from datetime import date
from timetable.models import SpecialEvent

register = template.Library()


@register.simple_tag
def next_poster():
    try:
        return SpecialEvent.objects.filter(hide_date__gte=date.today()).exclude(poster="").order_by('sort_date')[0]
    except (SpecialEvent.DoesNotExist, IndexError):
        return None

@register.simple_tag
def upcoming_events():
    return SpecialEvent.objects.filter(hide_date__gte=date.today()).order_by('sort_date')[:5]