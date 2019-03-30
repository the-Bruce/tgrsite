from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def can_manage(member, rpg):
    # whether given user has permission to manage given rpg
    # Not used as a tag - when this logic is changed be sure to update detail.html!
    return (member == rpg.creator) or (member in list(rpg.game_masters.all()))


# todo: assignment tag is deprecated
@register.simple_tag(takes_context=True)
def is_player(context, rpg):
    return rpg.members.filter(id=context.request.user.member.id)


@register.simple_tag
def rpg_url():
    return reverse('rpg_tag', args=['rpg'])


@register.simple_tag
def rpgs_root():
    return reverse('rpgs')
