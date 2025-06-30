from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import MediaFile
import os
from django.core.files import File
from django.conf import settings
from django.utils.safestring import mark_safe

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'uploaded_at', 'preview')
    list_filter = ('uploaded_at',)
    search_fields = ('name', 'description', 'file')
    list_editable = ()
    readonly_fields = ('uploaded_at', 'uploaded_by', 'preview')
    actions = []
    change_list_template = 'admin/media_manager/mediafile/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-media/', self.admin_site.admin_view(self.import_media_view), name='mediafile-import-media'),
        ]
        return custom_urls + urls

    def import_media_view(self, request):
        media_root = settings.MEDIA_ROOT
        imported = 0
        # Получаем множество (имя, размер) уже импортированных файлов
        existing_files = set()
        for mf in MediaFile.objects.all():
            if mf.file and mf.file.name and mf.file.size:
                existing_files.add((os.path.basename(mf.file.name), mf.file.size))
        for root, dirs, files in os.walk(media_root):
            if os.path.relpath(root, media_root).startswith('media_files'):
                continue
            for filename in files:
                abs_path = os.path.join(root, filename)
                file_size = os.path.getsize(abs_path)
                # Проверяем по имени и размеру
                if (filename, file_size) in existing_files:
                    continue
                rel_dir = os.path.relpath(root, media_root)
                db_path = os.path.join(rel_dir, filename).replace('\\', '/').replace('\\', '/')
                # Просто ссылка на файл, не копируем
                media_file = MediaFile(
                    name=filename,
                    description='' 
                )
                media_file.file.name = db_path
                media_file.save()
                imported += 1
        self.message_user(request, f'Импортировано файлов: {imported}', messages.SUCCESS)
        return redirect('..')

    def preview(self, obj):
        if obj.file and obj.file.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            url = obj.file.url
            html = (
                f'<a href="{url}" target="_blank" style="display:inline-block;">'
                f'<img src="{url}" style="max-height:48px;max-width:80px;border:1px solid #ccc;">'
                f'</a>'
            )
            return mark_safe(html)
        return ''
    preview.short_description = 'Превью'
    preview.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        try:
            super().delete_model(request, obj)
        except Exception as e:
            from django.core.exceptions import ValidationError
            if isinstance(e, ValidationError):
                self.message_user(request, e.messages[0], level=messages.ERROR)
            else:
                raise

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            try:
                obj.delete()
            except Exception as e:
                from django.core.exceptions import ValidationError
                if isinstance(e, ValidationError):
                    self.message_user(request, e.messages[0], level=messages.ERROR)
                else:
                    raise
