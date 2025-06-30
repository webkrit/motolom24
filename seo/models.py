"""Модели для приложения SEO управления."""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class SEOSettings(models.Model):
    """Общие SEO-настройки сайта."""
    site_name = models.CharField(
        max_length=100, default='motolom24', verbose_name='Название сайта'
    )
    default_title = models.CharField(
        max_length=60, blank=True, verbose_name='Заголовок по умолчанию',
        help_text='Заголовок для страниц без собственного title'
    )
    default_description = models.TextField(
        max_length=160, blank=True, verbose_name='Описание по умолчанию',
        help_text='Описание для страниц без собственного description'
    )
    default_keywords = models.CharField(
        max_length=255, blank=True, verbose_name='Ключевые слова по умолчанию',
        help_text='Ключевые слова для страниц без собственных keywords'
    )
    google_analytics = models.CharField(
        max_length=50, blank=True, verbose_name='Google Analytics ID',
        help_text='G-XXXXXXXXXX или UA-XXXXXXXX-X'
    )
    yandex_metrika = models.CharField(
        max_length=50, blank=True, verbose_name='Яндекс.Метрика ID',
        help_text='XXXXXXXX'
    )
    robots_txt = models.TextField(
        blank=True, verbose_name='Robots.txt',
        help_text='Содержимое файла robots.txt'
    )
    
    class Meta:
        verbose_name = 'SEO настройки'
        verbose_name_plural = 'SEO настройки'
    
    def __str__(self):
        return f'SEO настройки {self.site_name}'
    
    @classmethod
    def get_settings(cls):
        """Получить настройки SEO (создать если не существуют)."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class SEOItem(models.Model):
    """SEO-информация для любого объекта."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    url = models.CharField(max_length=255, verbose_name='URL')
    title = models.CharField(max_length=60, blank=True, verbose_name='Title')
    description = models.TextField(max_length=160, blank=True, verbose_name='Description')
    keywords = models.CharField(max_length=255, blank=True, verbose_name='Keywords')
    h1 = models.CharField(max_length=100, blank=True, verbose_name='H1')
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        verbose_name = 'SEO элемент'
        verbose_name_plural = 'SEO элементы'
        unique_together = ['content_type', 'object_id']
    
    def __str__(self):
        return f'SEO для {self.content_type.model}: {self.url}'


class SEOLog(models.Model):
    """Лог изменений SEO-информации."""
    ACTION_CHOICES = [
        ('create', 'Создание'),
        ('update', 'Обновление'),
        ('delete', 'Удаление'),
    ]
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name='Действие')
    field_name = models.CharField(max_length=50, verbose_name='Поле')
    old_value = models.TextField(blank=True, verbose_name='Старое значение')
    new_value = models.TextField(blank=True, verbose_name='Новое значение')
    user = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Пользователь'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    
    class Meta:
        verbose_name = 'SEO лог'
        verbose_name_plural = 'SEO логи'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'{self.get_action_display()} {self.content_type.model} #{self.object_id}'
