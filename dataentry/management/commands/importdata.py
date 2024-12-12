from django.db import DataError
from django.core.management import BaseCommand, CommandError
from django.core.management.base import CommandParser
from django.apps import apps
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
        model = None
        counter = 0

        # Search for the model across all installed apps
        for app_config in apps.get_app_configs():
            try: 
                model = apps.get_model(app_config.label, model_name)
                break

            except LookupError:
                continue
        
        if not model:
            raise CommandError(f"Model: '{model_name}' not found in any app")
        
    
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            model_fields = [field.name for field in model._meta.fields if field.name != 'id']
            csv_header = reader.fieldnames
            if csv_header != model_fields:                       # compare csv header with model's field names
                raise DataError(f"CSV file doesn't match with the {model_name} table fields")
                 
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
