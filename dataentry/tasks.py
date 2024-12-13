from awd_main.celery import app
import time 
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notifications


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
    message = 'Your data import has been seccessfull!'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notifications(mail_subject=mail_subject, message=message, to_email=to_email)

    return 'Data imported successfully'