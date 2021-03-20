from django.core.management.base import BaseCommand

from users.models import Member
from users.achievements import give_achievement_at, age_achievements


class Command(BaseCommand):
    help = 'Awards achievements to match newer rules'

    def handle(self, *args, **options):
        for m in Member.objects.all():
            rpgs = m.rpgs_owned.order_by("created_at")
            if len(rpgs) > 0:
                give_achievement_once(m, "first_event", rpgs[0].created_at)
            if len(rpgs) > 4:
                give_achievement_once(m, "five_events", rpgs[4].created_at)
            age_achievements(m)

        self.stdout.write('Achievements Migrated')
