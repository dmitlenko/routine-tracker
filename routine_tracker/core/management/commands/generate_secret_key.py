from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Generate secret key for the project'

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        self.stdout.write('Generated secret key:')
        self.stdout.write(self.style.WARNING(secret_key))
