from unittest.mock import Base
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = "Greets the user"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help="Specifies user name")

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(f"Hello {kwargs['name']}! Good morning"))
