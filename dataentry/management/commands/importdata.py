from django.core.management import BaseCommand
from dataentry.utils import check_csv_errros
from django.db import transaction
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
        objects = []

        # check for errors in csv
        model = check_csv_errros(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                obj = model(**row)
                objects.append(obj)

            with transaction.atomic():
                model.objects.bulk_create(objects, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f"Data imported from CSV successfully! {len(objects)} records were created"))


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
