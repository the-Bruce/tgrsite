from django.db.models import Count
from django.core.management.base import BaseCommand

from messaging.models import MessageThread


# Removes empty chats.
class Command(BaseCommand):
    help = 'Removes empty chats'

    def handle(self, *args, **options):
        MessageThread.objects.annotate(Count("message")).filter(message__count=0).all().delete()
        self.stdout.write('Messages Thread Cleaned')
