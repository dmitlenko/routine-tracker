import sys
import time

from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait for the database to be available"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--poll-seconds", type=float, default=3)
        parser.add_argument("--max-retries", type=int, default=60)

    def handle(self, *args, **options):
        max_retries = options["max_retries"]
        poll_seconds = options["poll_seconds"]

        self.stdout.write("Waiting for the database...")

        for _ in range(max_retries):
            try:
                connection.ensure_connection()
            except OperationalError:
                self.stdout.write(f"Database is not available. Retrying in {poll_seconds} seconds...")
                time.sleep(poll_seconds)
            else:
                self.stdout.write(self.style.SUCCESS("Database is available!"))
                break
        else:
            self.stdout.write(self.style.ERROR("Database is not available!"))
            sys.exit(1)
