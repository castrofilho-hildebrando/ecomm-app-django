from django.core.management.base import BaseCommand
import asyncio
from infrastructure.outbox.django_outbox_dispatcher import DjangoOutboxDispatcher


class Command(BaseCommand):
    help = 'Process outbox events'

    def handle(self, *args, **options):
        dispatcher = DjangoOutboxDispatcher()
        asyncio.run(dispatcher.dispatch())
        self.stdout.write(self.style.SUCCESS('Outbox events processed'))