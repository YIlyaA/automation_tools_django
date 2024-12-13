from django.http import HttpResponse
from django.shortcuts import render
from dataentry.tasks import celery_test_task

# Create your views here.
def home(request):
    return render(request, 'home.html')

def celery_test(request):
    # for test execute a time consuming task here:
    celery_test_task.delay()
    return HttpResponse('<h3>Function executed successfully</h3>')