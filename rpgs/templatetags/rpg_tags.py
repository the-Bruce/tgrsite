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

# this is all one big horrible hack around the URL system......
@register.simple_tag
def add_tags(url, tag):
	arr = tags_arr(url)
	arr.append(tag)
	arr = list(set(arr))
	arr = get_non_tags(url) + arr
	return '/'.join(arr)

@register.simple_tag
def tags_list(url):
	arr = tags_arr(url)
	r = ' / '.join(arr)
	if r == '':
		r = 'None'
	return r

def get_non_tags(url):
	r = url.split('/')[1:3]
	return r

def tags_arr(url):
	arr = url.split('/')[3:-1]
	return arr
