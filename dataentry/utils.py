from types import NoneType
from django.apps import apps
from django.core.management import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os
from django.conf import settings

from emails.models import Email, Sent

def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'Upload', 'User']

    custom_models = []

    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__) 
    return custom_models


def check_csv_errros(file_path, model_name):
    model = None
    # Search for the model across all installed apps
    for app_config in apps.get_app_configs():
        try: 
            model = apps.get_model(app_config.label, model_name)
            break

        except LookupError:
            continue
    
    # if there is no model - raise error
    if not model:
        raise CommandError(f"Model: '{model_name}' not found in any app")
    
    # take the model fields to compare with the fields in the csv file 
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            if csv_header != model_fields:                       # compare csv header with model's field names
                raise DataError(f"CSV file doesn't match with the {model_name} table fields")
            
    except Exception as e:
        raise e
    
    return model


def send_email_notifications(mail_subject, message, to_email, attachment=None, email_id=NoneType()):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(subject=mail_subject, body=message, from_email=from_email, to=to_email)
        if attachment:
            mail.attach_file(attachment)

        mail.content_subtype = "html"
        mail.send()

        # Store the total sent email inside the Sent model
        email = Email.objects.get(pk=email_id)
        sent = Sent()
        sent.email = email
        sent.total_sent = email.email_list.count_emails()
        sent.save()

    except Exception as e:
        raise e


def generate_csv_file(model_name):
    # generate timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")  

    # define csv file name\path
    export_dir = 'exported_data'
    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path