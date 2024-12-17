from django.contrib import messages
from django.shortcuts import redirect, render

from emails.models import Subscriber
from emails.tasks import send_email_task
from .forms import EmailForm



# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()

            # Send an email
            mail_subject = request.POST.get("subject")
            message = request.POST.get("body")
            email_list = request.POST.get(
                "email_list"
            )  # print(email_list) ==> 1 (or any number, it's Foreign key id)

            # Access the selected email list
            email_list = (
                email_form.email_list
            )  # print(email_list) ==> Developers (or another field in List model)

            # Extract email addresses for the Subscriber model in the selected email list
            subscribers = Subscriber.objects.filter(email_list=email_list)

            to_email = [
                email.email_address for email in subscribers
            ]  # print(to_email) ==>  ['email1@gmail.com', 'email2@gmail.com', ...]

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None

            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)

            # Display a success message
            messages.success(request, "Email sent successfully!")
            return redirect("send_email")
    else:
        email_form = EmailForm()
        context = {
            "email_form": email_form,
        }
    return render(request, "emails/send-email.html", context)


def track_click(request):
    return


def track_open(request):
    return

