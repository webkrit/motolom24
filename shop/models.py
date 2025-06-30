"""Модели для приложения shop интернет-магазина motolom24."""
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Category(models.Model):
    """Категория товаров с поддержкой вложенности."""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name='Родительская категория'
    )
    
    # SEO поля
    meta_title = models.CharField(
        max_length=60, blank=True, verbose_name='Meta Title',
        help_text='Заголовок страницы (до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=160, blank=True, verbose_name='Meta Description',
        help_text='Описание страницы (до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True, verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Строковое представление категории."""
        return self.name

    def get_meta_title(self):
        """Получить meta title или название категории."""
        return self.meta_title or self.name

    def get_meta_description(self):
        """Получить meta description."""
        return self.meta_description

class Product(models.Model):
    """Модель товара."""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    image = models.ImageField(
        upload_to='products/', blank=True, null=True, verbose_name='Фото'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    # SEO поля
    meta_title = models.CharField(
        max_length=60, blank=True, verbose_name='Meta Title',
        help_text='Заголовок страницы (до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=160, blank=True, verbose_name='Meta Description',
        help_text='Описание страницы (до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True, verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def __str__(self):
        """Строковое представление товара."""
        return self.name

    def get_meta_title(self):
        """Получить meta title или название товара."""
        return self.meta_title or self.name

    def get_meta_description(self):
        """Получить meta description или описание товара."""
        return self.meta_description or self.description[:160]

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            self.available = False
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/gallery/', verbose_name='Изображение')
    alt = models.CharField(max_length=255, blank=True, verbose_name='Альтернативный текст')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Галерея изображений'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.product.name} — {self.alt or self.image.name}"

class StaticPage(models.Model):
    """Модель для статичных страниц."""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = RichTextUploadingField(verbose_name='Содержание', config_name='bootstrap')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    # SEO поля
    meta_title = models.CharField(
        max_length=60, blank=True, verbose_name='Meta Title',
        help_text='Заголовок страницы (до 60 символов)'
    )
    meta_description = models.TextField(
        max_length=160, blank=True, verbose_name='Meta Description',
        help_text='Описание страницы (до 160 символов)'
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True, verbose_name='Meta Keywords',
        help_text='Ключевые слова через запятую'
    )

    class Meta:
        verbose_name = 'Статичная страница'
        verbose_name_plural = 'Статичные страницы'
        ordering = ['title']

    def __str__(self):
        """Строковое представление страницы."""
        return self.title

    def get_meta_title(self):
        """Получить meta title или заголовок страницы."""
        return self.meta_title or self.title

    def get_meta_description(self):
        """Получить meta description."""
        return self.meta_description

class Banner(models.Model):
    """Баннер для слайдера на главной странице."""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    image = models.ImageField(upload_to='banners/', verbose_name='Изображение')
    link = models.URLField(blank=True, verbose_name='Ссылка (опционально)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order', '-created']

    def __str__(self):
        return self.title

class MainPageSettings(models.Model):
    """Настройки главной страницы (единственная запись)."""
    products_count = models.PositiveIntegerField(
        default=8, verbose_name='Количество товаров в блоке "Последние поступления"'
    )
    text_block = RichTextField(
        blank=True, verbose_name='Текстовый блок на главной', config_name='bootstrap'
    )
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Настройки главной страницы'
        verbose_name_plural = 'Настройки главной страницы'

    def __str__(self):
        return 'Настройки главной страницы'

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

class MenuItem(models.Model):
    """Пункт главного меню сайта."""
    title = models.CharField(max_length=100, verbose_name='Название')
    url = models.CharField(max_length=255, verbose_name='Ссылка')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name='Родительский пункт')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    new_tab = models.BooleanField(default=False, verbose_name='Открывать в новой вкладке')

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['parent__id', 'order', 'title']

    def __str__(self):
        return self.title

class FooterSettings(models.Model):
    """Настройки подвала сайта (единственная запись)."""
    text_block = RichTextField(
        blank=True, verbose_name='Текстовый блок подвала', config_name='bootstrap'
    )
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Настройки подвала'
        verbose_name_plural = 'Настройки подвала'

    def __str__(self):
        return 'Настройки подвала сайта'

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

class SiteSettings(models.Model):
    """Глобальные настройки сайта (логотип и др.)."""
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Логотип')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
