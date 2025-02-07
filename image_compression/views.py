from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CompressImageForm
from PIL import Image
import io

# Create your views here.
def compress(request):
    user = request.user
    if request.method == "POST":
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']

            compressed_image = form.save(commit=False)   # temporary save form `commit=False`
            compressed_image.user = user
            
            # perform compression
            img = Image.open(original_img)

            output_format = img.format            # set image formats dynamically
            buffer = io.BytesIO()                             # empty buffor to represent sequence of bytes
            img.save(buffer, format=output_format, quality=quality)  # save image to blank buffor
            buffer.seek(0)                                    # set to 0 position

            # save the compressed image inside the model
            compressed_image.compressed_img.save(             # compressed_img - fieldname
                f'compressed_{original_img}', buffer
            )  

            # Automatically downlaod the compressed file
            response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')  # getvalue() - binary data of the buffer
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'  # send the file using browser
            return response
            # return redirect('compress')
    else:
        form = CompressImageForm()
        context = {
            'form': form,
        }
        return render(request, 'image_compression/compress.html', context)