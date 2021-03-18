from django.core.management.base import BaseCommand

from users.models import Member
from users.achievements import give_achievement_once


class Command(BaseCommand):
    help = 'Awards achievements to match newer rules'

    def handle(self, *args, **options):
        for m in Member.objects.all():
            rpgs = m.rpgs_owned.count()
            if rpgs > 0:
                give_achievement_once(m, "first_event")
            if rpgs > 4:
                give_achievement_once(m, "five_events")

        self.stdout.write('Achievements Migrated')
