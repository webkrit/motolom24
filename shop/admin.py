"""Admin configuration for shop app."""
from django.contrib import admin
from .models import (
    Category, Product, StaticPage, Banner, MainPageSettings, MenuItem,
    FooterSettings, SiteSettings, ProductImage
)
from django import forms
from django.forms.widgets import ClearableFileInput
from django.utils.text import slugify
from django.utils.crypto import get_random_string

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('SEO информация', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

class MultiImageInput(ClearableFileInput):
    """Виджет для множественной загрузки изображений."""

    allow_multiple_selected = True

    def __init__(self, *args, **kwargs):
        """Инициализация виджета с поддержкой multiple."""
        kwargs['attrs'] = kwargs.get('attrs', {})
        kwargs['attrs']['multiple'] = True
        super().__init__(*args, **kwargs)

class ProductImageInlineForm(forms.ModelForm):
    """Форма для инлайна изображений товара."""

    class Meta:
        """Мета-класс для ProductImageInlineForm."""
        model = ProductImage
        fields = ('image', 'alt', 'order')
        widgets = {
            'image': MultiImageInput(),
        }

class ProductImageInline(admin.TabularInline):
    """Инлайн для изображений товара в админке."""

    model = ProductImage
    extra = 1
    fields = ('image', 'alt', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Показывает превью изображения в админке."""
        if obj.image:
            return (
                f'<img src="{obj.image.url}" style="max-height:48px;max-width:80px;">'
            )
        return ''

    image_preview.short_description = 'Превью'
    image_preview.allow_tags = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для модели Product."""
    list_display = ('name', 'category', 'price', 'quantity', 'available', 'created')
    list_editable = ('quantity', 'available')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'image', 'description', 'price', 'quantity', 'available')
        }),
        ('SEO информация', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProductImageInline]
    actions = ['duplicate_product']

    @admin.action(description='Дублировать выбранные товары')
    def duplicate_product(self, request, queryset):
        for product in queryset:
            images = list(product.images.all())
            new_name = f'{product.name} (Копия)'
            new_slug = slugify(f'{product.name}-{get_random_string(6)}')
            product.pk = None
            product.id = None
            product.name = new_name
            product.slug = new_slug
            product.save()
            for img in images:
                img.pk = None
                img.id = None
                img.product = product
                img.save()
        self.message_user(request, 'Выбранные товары успешно продублированы.')

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'updated')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('created', 'updated')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'is_active')
        }),
        ('SEO информация', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'updated')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)
    list_filter = ('is_active',)
    ordering = ('order', '-created')

@admin.register(MainPageSettings)
class MainPageSettingsAdmin(admin.ModelAdmin):
    list_display = ('products_count', 'updated')
    readonly_fields = ('updated',)
    fieldsets = (
        (None, {
            'fields': ('products_count', 'text_block', 'updated')
        }),
    )
    def has_add_permission(self, request):
        return not MainPageSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
    def changelist_view(self, request, extra_context=None):
        settings, created = MainPageSettings.objects.get_or_create(pk=1)
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(
            reverse('admin:shop_mainpagesettings_change', args=[settings.pk])
        )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'order', 'is_active', 'new_tab')
    list_editable = ('order', 'is_active', 'new_tab')
    list_filter = ('is_active', 'parent')
    search_fields = ('title', 'url')
    ordering = ('parent__id', 'order', 'title')

@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    list_display = ('updated',)
    readonly_fields = ('updated',)
    fieldsets = (
        (None, {
            'fields': ('text_block', 'updated')
        }),
    )
    def has_add_permission(self, request):
        return not FooterSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
    def changelist_view(self, request, extra_context=None):
        settings, created = FooterSettings.objects.get_or_create(pk=1)
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(
            reverse('admin:shop_footersettings_change', args=[settings.pk])
        )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('logo', 'updated')
    readonly_fields = ('updated',)
    fieldsets = (
        (None, {
            'fields': ('logo', 'updated')
        }),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
    def changelist_view(self, request, extra_context=None):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(
            reverse('admin:shop_sitesettings_change', args=[settings.pk])
        )

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
