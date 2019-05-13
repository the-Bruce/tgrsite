from django.core.management.base import BaseCommand

from notifications.tasks import doSummaryNotificationMailings


class Command(BaseCommand):
    def handle(self, *args, **options):
        doSummaryNotificationMailings()
