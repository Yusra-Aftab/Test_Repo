from django.http import JsonResponse
from django.http import JsonResponse
from .models import UploadedFile


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('mp4File'):
        uploaded_file = UploadedFile(file=request.FILES['mp4File'])
        uploaded_file.save()
        return JsonResponse({'message': 'File uploaded successfully'})
    return JsonResponse({'message': 'File upload failed'}, status=400)
