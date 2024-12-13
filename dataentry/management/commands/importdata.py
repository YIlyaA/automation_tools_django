from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from django.apps import apps
from dataentry.utils import check_csv_errros
import csv


# Proposed command: py manage.py importdata <file_path.csv> <model_name>
class Command(BaseCommand):
    help = "Import data from csv file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to CSV file")
        parser.add_argument("model_name", type=str, help="Name of the model") 

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_name = kwargs["model_name"].capitalize()
        counter = 0

        # check for errors in csv
        model = check_csv_errros(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                model.objects.create(**row)
                counter += 1

        self.stdout.write(self.style.SUCCESS(f"Data imported from CSV successfully! {counter} records were created"))


##################### EXAMPLE ####################
# # Proposed command: py manage.py importdata <file_path.csv>

# from dataentry.models import Student

# class Command(BaseCommand):
#     help = "Import data from csv file"

#     def add_arguments(self, parser):
#         parser.add_argument("file_path", type=str, help="Path to CSV file")

#     def handle(self, *args, **kwargs):
#         file_path = kwargs["file_path"]
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if not Student.objects.filter(roll_no=row["roll_no"]).exists():
#                     Student.objects.create(**row)

#         self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully"))
