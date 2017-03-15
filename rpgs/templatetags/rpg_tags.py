from django import template
from rpgs.models import Rpg

register = template.Library()

@register.simple_tag
def can_manage(member, rpg):
	# whether given user has permission to manage given rpg
	# Not used as a tag - when this logic is changed be sure to update detail.html!
	return (member == rpg.creator) or (member in list(rpg.game_masters.all()))

@register.assignment_tag(takes_context=True)
def is_player(context, rpg):
	return rpg.members.filter(id=context.request.user.member.id)
