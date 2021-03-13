from users.models import Member, Achievement, AchievementAward
from notifications.utils import notify
from notifications.models import NotifType

def give_achievement(member : Member, trigger : str):
    achiev, _ = Achievement.objects.get_or_create(
            trigger_name__iexact=trigger,
            trigger_name=trigger,
            defaults = {'name': trigger.title()})
    award = AchievementAward.objects.create(member=member, achievement=achiev)
    achiev_name = f"You got an achievement: {achiev.name}!"
    notify(member, NotifType.ACHIEVEMENTS, achiev_name, "/user/me/")
    return award

def give_achievement_once(member : Member, trigger : str):
    achiev, _ = Achievement.objects.get_or_create(
            trigger_name__iexact=trigger,
            trigger_name=trigger,
            defaults = {'name': trigger.title()})
    award, created = AchievementAward.objects.get_or_create(member=member, achievement=achiev)
    if created:
        achiev_name = f"You got an achievement: {achiev.name}!"
        notify(member, NotifType.ACHIEVEMENTS, achiev_name, "/user/me/")
    return award
