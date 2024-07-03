from django.core.management.base import BaseCommand
from authlib.task import cleanup_expired_tokens

class Command(BaseCommand):
    help = 'Cleanup expired tokens'

    def handle(self, *args, **kwargs):
        cleanup_expired_tokens()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up expired tokens'))
