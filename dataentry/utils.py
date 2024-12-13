from django.apps import apps
from django.core.management import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings

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


def send_email_notifications(mail_subject, message, to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(subject=mail_subject, body=message, from_email=from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e
