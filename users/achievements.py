from users.models import Member, Achievement, AchievementAward
from notifications.utils import notify
from notifications.models import NotifType

from django.utils import timezone


def give_achievement(member: Member, trigger: str):
    achiev, _ = Achievement.objects.get_or_create(
        trigger_name__iexact=trigger,
        trigger_name=trigger,
        defaults={'name': trigger.title().replace("_", " ")})
    award = AchievementAward.objects.create(member=member, achievement=achiev)
    achiev_name = f"You got an achievement: {achiev.name}!"
    notify(member, NotifType.ACHIEVEMENTS, achiev_name, "/user/me/")
    return award


def give_achievement_once(member: Member, trigger: str):
    achiev, _ = Achievement.objects.get_or_create(
        trigger_name__iexact=trigger,
        trigger_name=trigger,
        defaults={'name': trigger.title()})
    return give_this_achievement_once(member, achiev)


def give_this_achievement_once(member: Member, achiev: Achievement):
    award, created = AchievementAward.objects.get_or_create(member=member, achievement=achiev)
    if created:
        achiev_name = f"You got an achievement: {achiev.name}!"
        notify(member, NotifType.ACHIEVEMENTS, achiev_name, "/user/me/")
    return award


age_awards = {1: "one_year", 2: "two_years", 3: "three_years", 4: "four_years", 5: "five_years", 10: "resurrected"}


def age_achievements(member: Member):
    date = member.equiv_user.date_joined
    timesince = timezone.now() - date
    # This will be inaccurate every 400 years or something, so is good enough.
    # The alternative is adding a new dependency.
    years = timesince.days / 365.2425
    for i in age_awards.keys():
        if years >= i:
            give_achievement_once(member, age_awards[i])
