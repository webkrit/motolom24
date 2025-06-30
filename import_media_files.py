import os
from django.core.files import File
from django.conf import settings
from media_manager.models import MediaFile

MEDIA_ROOT = settings.MEDIA_ROOT

# Собираем все файлы в media/ и подпапках
for root, dirs, files in os.walk(MEDIA_ROOT):
    for filename in files:
        rel_dir = os.path.relpath(root, MEDIA_ROOT)
        rel_file = os.path.join(rel_dir, filename) if rel_dir != '.' else filename
        db_path = os.path.join(rel_dir, filename).replace('\\', '/').replace('\\', '/')
        # Проверяем, есть ли уже такой файл в базе
        if not MediaFile.objects.filter(file=f"media_files/{db_path}").exists():
            abs_path = os.path.join(root, filename)
            with open(abs_path, 'rb') as f:
                media_file = MediaFile(
                    name=filename,
                    description='',
                    is_active=True
                )
                # Сохраняем файл в FileField (upload_to='media_files/')
                media_file.file.save(db_path, File(f), save=True)
            print(f'Импортирован: {db_path}')
        else:
            print(f'Уже в базе: {db_path}') 