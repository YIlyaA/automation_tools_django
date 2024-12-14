from django.core.management import call_command
from django.shortcuts import render, redirect
from .utils import check_csv_errros, get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from .tasks import import_data_task, export_data_task

# Create your views here.
def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # construct the full path
        relative_path = str(upload.file.url)
        base_url =str(settings.BASE_DIR)
        file_path = base_url + relative_path

        # check for the CSV errors
        try:
            check_csv_errros(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # handle the importdata task
        import_data_task.delay(file_path, model_name)

        # show message to the user
        messages.success(request, 'Your data is being imported. You will be notified once it is done')

        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/import_data.html', context=context)


def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get('model_name')

        # call export data task
        export_data_task.delay(model_name)

        # show message to the user
        messages.success(request, 'Your data is being exported. You will be notified once it is done')
        
        return redirect('export_data')
    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models': custom_models,
        }
    return render(request, 'dataentry/exportdata.html', context)