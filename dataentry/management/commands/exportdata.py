from django.core.management import BaseCommand
import csv
from django.apps import apps
from dataentry.utils import generate_csv_file


# Proposed command: py manage.py exportdata <model_name>
class Command(BaseCommand):
    help = "Export data from the database to a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"].capitalize()
        model = None

        # search throw all the installed apps for the model
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break

            except LookupError:
                pass

        if not model:
            self.stderr.write(self.style.ERROR(f"Model: '{model_name}' not found in any app"))
            return

        data = model.objects.all()  # fetch data from db

        # generate csv file path
        file_path = generate_csv_file(model_name)

        with open(file_path, "w", newline="") as file:  # open csv file and write data
            writer = csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])  # headers

            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS("Data was exported successfully"))


################### EXAMPLE ########################
# from dataentry.models import Student
# # Proposed command: py manage.py exportdata
# class Command(BaseCommand):
#     help = "Export data from db to CSV file"

#     def handle(self, *args, **kwargs):
#         students = Student.objects.all()  # fetch data from db
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")  # generate timestamp of current date and time

#         # define csv file name\path
#         file_path = f'exported_students_data_{timestamp}.csv'

#         with open(file_path, 'w', newline='') as file:   # open csv file and write data
#             writer = csv.writer(file)

#             writer.writerow(['Roll No', 'Name', 'Age'])  # headers

#             for student in students:
#                 writer.writerow([student.roll_no, student.name, student.age])


#         self.stdout.write(self.style.SUCCESS("Data was exported successfully"))
