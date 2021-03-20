from django.core.management.base import BaseCommand

from users.models import Member
from users.achievements import give_achievement_once, age_achievements


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
            first_thread = m.thread_set.order_by("pub_date").first()
            if first_thread:
                give_achievement_once(m, "created_thread", first_thread.pub_date)
            first_response = m.response_set.order_by("pub_date").first()
            if first_response:
                give_achievement_once(m, "replied_forum", first_response.pub_date)
            first_message = m.message_set.order_by("timestamp").first()
            if first_message:
                give_achievement_once(m, "messaged", first_message.timestamp)

        self.stdout.write('Achievements Migrated')
