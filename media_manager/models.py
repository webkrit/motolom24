from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.apps import apps
from django.db.models.fields.files import ImageFieldFile
import os
from django.core.files import File
from django.core.exceptions import ValidationError

# Create your models here.

class MediaFile(models.Model):
    """Медиафайл проекта (изображение, документ и т.д.)."""
    name = models.CharField(max_length=255, verbose_name='Название')
    file = models.FileField(upload_to='media_files/', verbose_name='Файл')
    description = models.TextField(blank=True, verbose_name='Описание')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    uploaded_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Кто загрузил')

    class Meta:
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'
        ordering = ['-uploaded_at', 'name']

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=MediaFile)
def check_file_usage_on_mediafile_delete(sender, instance, **kwargs):
    if instance.file:
        file_path = instance.file.name
        used_in = []
        for model in apps.get_models():
            if model._meta.label == 'media_manager.MediaFile':
                continue
            for field in model._meta.get_fields():
                if hasattr(field, 'attname') and hasattr(model, field.attname):
                    if hasattr(field, 'upload_to') and hasattr(field, 'storage'):
                        qs = model.objects.filter(**{f"{field.name}": file_path})
                        if qs.exists():
                            for obj in qs:
                                used_in.append(f"{model._meta.label} (id={obj.pk}, поле={field.name})")
        if used_in:
            msg = f'Файл {file_path} не может быть удалён, так как используется в: ' + ", ".join(used_in)
            raise ValidationError(msg)
        # Если не используется — удаляем
        instance.file.delete(save=False)

@receiver(post_save)
def auto_add_image_to_mediafile(sender, instance, **kwargs):
    # Исключаем саму модель MediaFile, чтобы не было рекурсии
    if sender._meta.label == 'media_manager.MediaFile':
        return
    for field in instance._meta.get_fields():
        # Только ImageField
        if hasattr(field, 'attname') and hasattr(instance, field.attname):
            filefield = getattr(instance, field.attname)
            if isinstance(filefield, ImageFieldFile) and filefield and filefield.name:
                from .models import MediaFile
                import os
                # Проверка по имени и размеру
                file_name = os.path.basename(filefield.name)
                file_size = filefield.size if hasattr(filefield, 'size') else None
                if file_size is None:
                    try:
                        file_size = filefield.file.size
                    except Exception:
                        continue
                exists = MediaFile.objects.filter(
                    name=file_name
                ).filter(
                    file__endswith=file_name
                ).filter(
                    file__isnull=False
                ).filter(
                    file__exact=filefield.name
                ).exists()
                if not exists:
                    if not MediaFile.objects.filter(file=filefield.name).exists():
                        mf = MediaFile(name=file_name, description='')
                        mf.file.name = filefield.name  # Просто ссылка
                        mf.save()
