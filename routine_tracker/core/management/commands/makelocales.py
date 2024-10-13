from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create locale files for the project'

    def handle(self, *args, **options):
        # Create locale files for the project
        # The locale files are created for all languages
        # defined in the LANGUAGES setting
        locales = [item[0] for item in settings.LANGUAGES]

        # Call the makemessages command for each locale
        call_command(
            'makemessages',
            locale=locales,
            ignore=['venv'],
            verbosity=1,
            no_obsolete=True,
        )
