from django import template

from django.contrib.auth.models import User
from users.models import Member

register = template.Library()


@register.simple_tag
def get_conversation_name(thread_, me):
    if thread_.title:
        return thread_.title
    else:
        if isinstance(me, User):
            me = me.username
        elif isinstance(me, Member):
            me = me.equiv_user.username

        participants = [str(x) for x in thread_.participants.all()]

        if me in participants and len(participants) > 1:
            participants.remove(me)
        title = ', '.join(participants)
        if len(title) > 50:
            title = title[0:50]
            title = title.strip() + "..."
        return title
