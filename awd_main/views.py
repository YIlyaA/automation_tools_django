from django.contrib import auth, messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from dataentry.tasks import celery_test_task
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def celery_test(request):
    # for test execute a time consuming task here:
    celery_test_task.delay()
    return HttpResponse('<h3>Function executed successfully</h3>')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful")
            return redirect('login')
        else:
            context = {'form': form,}
            return render(request, "register.html", context)
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
    return render(request, "register.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                # messages.success(request, "Login successful")
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }

    return render(request, "login.html", context)


def logout(request):
    return