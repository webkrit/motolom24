from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import SEOSettings, SEOItem, SEOLog


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    """Админка для SEO-настроек сайта."""
    list_display = ('site_name', 'default_title', 'google_analytics', 'yandex_metrika')
    fieldsets = (
        ('Основные настройки', {
            'fields': ('site_name', 'default_title', 'default_description', 'default_keywords')
        }),
        ('Аналитика', {
            'fields': ('google_analytics', 'yandex_metrika'),
            'classes': ('collapse',)
        }),
        ('Файлы', {
            'fields': ('robots_txt',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Запретить создание дополнительных настроек."""
        return not SEOSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Запретить удаление настроек."""
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Перенаправить на редактирование единственной записи."""
        settings, created = SEOSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:seo_seosettings_change', args=[settings.pk])
        )


@admin.register(SEOItem)
class SEOItemAdmin(admin.ModelAdmin):
    """Админка для SEO-элементов с inline редактированием."""
    list_display = ('get_object_name', 'url', 'title', 'description', 'keywords', 'updated')
    list_editable = ('title', 'description', 'keywords')
    list_filter = ('content_type', 'updated')
    search_fields = ('url', 'title', 'description', 'keywords')
    readonly_fields = ('content_type', 'object_id', 'url', 'created', 'updated')
    
    def get_object_name(self, obj):
        """Получить название объекта."""
        try:
            return str(obj.content_object)
        except:
            return f'{obj.content_type.model} #{obj.object_id}'
    get_object_name.short_description = 'Объект'
    
    def get_title(self, obj):
        """Получить title с подсветкой длины."""
        if obj.title:
            color = 'green' if len(obj.title) <= 60 else 'red'
            return format_html(
                '<span style="color: {};">{}</span> ({})',
                color, obj.title, len(obj.title)
            )
        return '-'
    get_title.short_description = 'Title'
    
    def get_description(self, obj):
        """Получить description с подсветкой длины."""
        if obj.description:
            color = 'green' if len(obj.description) <= 160 else 'red'
            return format_html(
                '<span style="color: {};">{}</span> ({})',
                color, obj.description[:50] + '...' if len(obj.description) > 50 else obj.description,
                len(obj.description)
            )
        return '-'
    get_description.short_description = 'Description'
    
    def get_keywords(self, obj):
        """Получить keywords."""
        return obj.keywords[:50] + '...' if obj.keywords and len(obj.keywords) > 50 else obj.keywords or '-'
    get_keywords.short_description = 'Keywords'
    
    def has_add_permission(self, request):
        """Запретить ручное создание SEO-элементов."""
        return False


@admin.register(SEOLog)
class SEOLogAdmin(admin.ModelAdmin):
    """Админка для логов SEO-изменений."""
    list_display = ('timestamp', 'get_object_name', 'action', 'field_name', 'user')
    list_filter = ('action', 'content_type', 'timestamp', 'user')
    search_fields = ('field_name', 'old_value', 'new_value')
    readonly_fields = ('content_type', 'object_id', 'action', 'field_name', 'old_value', 'new_value', 'user', 'timestamp')
    
    def get_object_name(self, obj):
        """Получить название объекта."""
        try:
            return str(obj.content_object)
        except:
            return f'{obj.content_type.model} #{obj.object_id}'
    get_object_name.short_description = 'Объект'
    
    def has_add_permission(self, request):
        """Запретить ручное создание логов."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Запретить редактирование логов."""
        return False


class SEOAdminSite(admin.AdminSite):
    """Кастомная админка для SEO-управления."""
    site_header = 'SEO Управление'
    site_title = 'SEO Панель'
    index_title = 'SEO Управление сайтом'


# Создаем экземпляр кастомной админки
seo_admin_site = SEOAdminSite(name='seo_admin')

# Регистрируем модели в кастомной админке
seo_admin_site.register(SEOSettings, SEOSettingsAdmin)
seo_admin_site.register(SEOItem, SEOItemAdmin)
seo_admin_site.register(SEOLog, SEOLogAdmin)
