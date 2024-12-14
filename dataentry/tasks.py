from awd_main.celery import app
import time 
from django.core.management import call_command
from django.conf import settings
from .utils import generate_csv_file, send_email_notifications


@app.task
def celery_test_task():
    time.sleep(10) # simulation of a time consuming task  

    # send an email (test)
    mail_subject = 'Test subject'
    message = 'This is test email'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notifications(mail_subject=mail_subject, message=message, to_email=to_email)

    return 'Email sent successfully!'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    
    # notify user by email
    mail_subject = 'Import Data Completed'
    message = 'Your data import has been successful!'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notifications(mail_subject=mail_subject, message=message, to_email=to_email)

    return 'Data imported successfully'


@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata',model_name)
    except Exception as e:
        raise e
    
    file_path = generate_csv_file(model_name)

    # Send email with attachment
    mail_subject = 'Export Data Successful'
    message = 'Your data export has been successful! Please find the attachment.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notifications(mail_subject=mail_subject, message=message, to_email=to_email, attachment=file_path)

    return 'Data exported successfully'