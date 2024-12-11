from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints Hello World"     # help function `py manage.py <file_name> --help`

    def handle(self, *args, **kwargs):    # we write a logic of this command in this function 
        self.stdout.write("Hello world")
