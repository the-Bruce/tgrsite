from django.core.management.base import BaseCommand
from django.db.models import Count

from notifications.tasks import doSummaryNotificationMailings
from messaging.models import MessageThread


class Command(BaseCommand):
    help = 'Performs all daily cleanup tasks'

    def handle(self, *args, **options):
        doSummaryNotificationMailings()
        MessageThread.objects.annotate(Count("message")).filter(message__count=0).all().delete()
        self.stdout.write('Messages Thread Cleaned')
