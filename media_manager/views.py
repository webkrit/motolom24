from django.shortcuts import render
from ckeditor_uploader.views import upload
from django.http import HttpResponse
from .models import MediaFile
import os
from django.core.files import File

# Create your views here.

def ckeditor_upload_create_mediafile(request):
    response = upload(request)
    # Если файл успешно загружен, создаём MediaFile
    if response.status_code == 200 and 'url' in response.content.decode():
        # Извлекаем путь к файлу из ответа
        import json
        data = json.loads(response.content.decode())
        file_url = data.get('url')
        if file_url:
            # file_url типа /media/uploads/xxx.jpg
            from django.conf import settings
            file_path = file_url.replace(settings.MEDIA_URL, '')
            abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(abs_path):
                # Проверяем, есть ли уже такой файл в MediaFile
                if not MediaFile.objects.filter(file=file_path).exists():
                    with open(abs_path, 'rb') as f:
                        mf = MediaFile(name=os.path.basename(file_path), description='')
                        mf.file.save(os.path.basename(file_path), File(f), save=True)
    return response
