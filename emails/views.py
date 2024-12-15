from django.shortcuts import render
from .forms import EmailForm

# Create your views here.
def send_email(request):
    if request.method == "POST":
        return
    else:
        email_form = EmailForm()
        context = {
            "email_form": email_form,
        }
    return render(request, "emails/send-email.html", context)