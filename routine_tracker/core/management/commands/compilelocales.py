from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Compile locale files for the project'

    def handle(self, *args, **options):
        # Compile locale files for the project
        locales = [item[0] for item in settings.LANGUAGES if item[0] != settings.LANGUAGE_CODE]

        # Call the makemessages command for each locale
        call_command(
            'compilemessages',
            ignore=['venv'],
            locale=locales,
            verbosity=1,
        )
