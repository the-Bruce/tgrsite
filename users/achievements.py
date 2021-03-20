from users.models import Member, Achievement, AchievementAward
from notifications.utils import notify
from notifications.models import NotifType

from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime


def get_achievement_from_trigger(trigger: str):
    achiev, _ = Achievement.objects.get_or_create(
        trigger_name__iexact=trigger,
        trigger_name=trigger,
        defaults={'name': trigger.title().replace("_", " ")})
    return achiev


def notify_achievement(member: Member, name: str):
    achiev_name = f"You got an achievement: {name}!"
    notify(member, NotifType.ACHIEVEMENTS, achiev_name, "/user/me/")


def give_achievement(member: Member, trigger: str, date: datetime = timezone.now()):
    achiev = get_achievement_from_trigger(trigger)
    award = AchievementAward.objects.create(member=member, achievement=achiev, achieved_at=date)
    notify_achievement(member, achiev.name)
    return award


def give_achievement_once(member: Member, trigger: str, date: datetime = timezone.now()):
    achiev = get_achievement_from_trigger(trigger)
    return give_this_achievement_once(member, achiev, date)


def give_this_achievement_once(member: Member, achiev: Achievement, date: datetime = timezone.now()):
    award, created = AchievementAward.objects.get_or_create(member=member, achievement=achiev, achieved_at=date)
    if created:
        notify_achievement(member, achiev.name)
    return award


age_awards = {1: "one_year", 2: "two_years", 3: "three_years", 4: "four_years", 5: "five_years", 10: "resurrected"}


def age_achievements(member: Member):
    date = member.equiv_user.date_joined
    timesince = relativedelta(timezone.now(), date)
    years = timesince.years
    for i in age_awards.keys():
        if years >= i:
            achieved_date = date + relativedelta(years=i)
            give_achievement_once(member, age_awards[i], achieved_date)
