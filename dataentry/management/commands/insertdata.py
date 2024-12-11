# add data to db using custom command

from django.core.management import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):

    help = "Insert data to database"

    def handle(self, *args, **kwargs):
        dataset = [
            {"roll_no": 1002, "name": "Sachin", "age": 21},
            {"roll_no": 1003, "name": "John", "age": 22},
            {"roll_no": 1006, "name": "Mikarena", "age": 23},
            {"roll_no": 1005, "name": "Mira", "age": 24},
        ]

        for data in dataset:
            roll_no = data["roll_no"]
            if not Student.objects.filter(roll_no=roll_no).exists():
                Student.objects.create(name=data["name"], roll_no=data["roll_no"], age=data["age"])
            else:
                self.stdout.write(self.style.WARNING(f"Student with {roll_no} already exists"))

        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))
