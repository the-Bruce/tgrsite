from django import template

register = template.Library()


@register.simple_tag
def get_participants_excluding_self(mthread, user):
    party = mthread.participants.all()
    party2 = [str(x) for x in party if user.username != x.equiv_user.username]
    if len(party2) == 0:
        party2 += [user.username]
    return ', '.join(party2)


@register.simple_tag
def get_conversation_name(convo, me):
    if convo.title != '':
        return convo.title

    arr = [str(x) for x in convo.participants.all()]

    if me in arr and len(arr) > 1:
        arr.remove(me)
    return ', '.join(arr)
