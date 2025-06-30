#!/usr/bin/env python
"""Скрипт для инициализации SEO-данных."""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motolom24.settings')
django.setup()

from django.contrib.sites.models import Site
from seo.models import SEOSettings
from shop.models import Category, Product, StaticPage


def init_seo():
    """Инициализация SEO-данных."""
    
    # Создаем или обновляем сайт
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': 'motolom24.ru',
            'name': 'motolom24 - Интернет-магазин мотоциклов'
        }
    )
    if created:
        print(f'Создан сайт: {site.name}')
    else:
        print(f'Сайт уже существует: {site.name}')
    
    # Создаем SEO-настройки
    seo_settings = SEOSettings.get_settings()
    seo_settings.site_name = 'motolom24'
    seo_settings.default_title = 'motolom24 - Интернет-магазин мотоциклов и запчастей'
    seo_settings.default_description = 'Купить мотоциклы, запчасти и аксессуары в интернет-магазине motolom24. Большой выбор, выгодные цены, доставка по России.'
    seo_settings.default_keywords = 'мотоциклы, запчасти, аксессуары, купить мотоцикл, мотоциклетные запчасти'
    seo_settings.robots_txt = """User-agent: *
Allow: /

# Запрещаем админку
Disallow: /admin/
Disallow: /seo-admin/

# Разрешаем sitemap
Sitemap: https://motolom24.ru/sitemap.xml
"""
    seo_settings.save()
    print('SEO-настройки созданы/обновлены')
    
    print('SEO-инициализация завершена успешно!')


if __name__ == '__main__':
    init_seo() 