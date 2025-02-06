from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import email
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from emails.models import Email, EmailTracking, Sent, Subscriber
from emails.tasks import send_email_task
from .forms import EmailForm



# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()

            # Send an email
            mail_subject = request.POST.get("subject")
            message = request.POST.get("body")
            email_list = request.POST.get(
                "email_list"
            )  # print(email_list) ==> 1 (or any number, it's Foreign key id)

            # Access the selected email list
            email_list = (
                email.email_list
            )  # print(email_list) ==>  (or another field in List model)

            # Extract email addresses for the Subscriber model in the selected email list
            subscribers = Subscriber.objects.filter(email_list=email_list)

            to_email = [
                email.email_address for email in subscribers
            ]  # print(to_email) ==>  ['email1@gmail.com', 'email2@gmail.com', ...]

            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id

            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id)

            # Display a success message
            messages.success(request, "Email sent successfully!")
            return redirect("send_email")
    else:
        email_form = EmailForm()
        context = {
            "email_form": email_form,
        }
        return render(request, "emails/send-email.html", context)


def track_click(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if the clicked field is already set or not
        url = request.GET.get("url")
        # check if the clicked_at field is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except:
        return HttpResponse("Email not found!")


def track_open(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if the opened field is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email opened successfully!")
        else:
            return HttpResponse("Email already opened!")
    except:
        return HttpResponse("Email not found!")


def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at')  #add total_sent to the Email model

    context = {
        "emails": emails,
    }
    return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)

    context = {
        "email": email,
        "total_sent": sent.total_sent,
    }
    return render(request, "emails/track_stats.html", context)