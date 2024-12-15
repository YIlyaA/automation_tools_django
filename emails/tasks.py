from awd_main.celery import app
from dataentry.utils import send_email_notifications


@app.task
def send_email_task(mail_subject, message, to_email, attachment):

    send_email_notifications(mail_subject, message, to_email, attachment)

    return 'Email sending task executed successfully.'