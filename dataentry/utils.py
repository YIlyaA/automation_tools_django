import hashlib
import time
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
from bs4 import BeautifulSoup
from requests import get

from emails.models import Email, EmailTracking, Sent, Subscriber

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


def send_email_notifications(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recepient_email in to_email:
            # Create EmalTracking record (only for Bulk Email Tool)
            new_message = message
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recepient_email)
                # generate unique id
                timestamp = str(time.time())
                data_to_hash = f"{recepient_email}{timestamp}"

                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id
                )

                # Generate the tracking pixel
                click_tracking_url = f"{settings.BASE_URL}/emails/track/click/{unique_id}/"
                open_tracking_url = f"{settings.BASE_URL}/emails/track/open/{unique_id}/"

                # Search for the links in the email body
                soup = BeautifulSoup(message, 'html.parser')
                urls = [a['href'] for a in soup.find_all('a', href=True)]

                # If there are links or urls in email body, we will inject our tracking url to that original link
                if urls:
                    for url in urls:
                        # make final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")
                else:
                    print("No links found in the email body")

                # Create email content with tracking pixel image
                open_tracking_image = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message += open_tracking_image

            mail = EmailMessage(subject=mail_subject, body=new_message, from_email=from_email, to=[recepient_email])
            if attachment:
                mail.attach_file(attachment)

            mail.content_subtype = "html"
            mail.send()
            
        # Store the total sent email inside the Sent model
        if email_id:
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