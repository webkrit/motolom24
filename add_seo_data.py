#!/usr/bin/env python
"""Скрипт для добавления SEO-информации к существующим данным."""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motolom24.settings')
django.setup()

from shop.models import Category, Product, StaticPage


def add_seo_data():
    """Добавить SEO-информацию к существующим данным."""
    
    # Обновляем категории
    categories_data = {
        'motorcycles': {
            'meta_title': 'Мотоциклы - Купить мотоцикл в Москве | motolom24',
            'meta_description': 'Купить мотоциклы в Москве. Большой выбор спортивных, круизеров, эндуро. Гарантия, доставка, кредит.',
            'meta_keywords': 'мотоциклы, купить мотоцикл, спортивные мотоциклы, круизеры, эндуро',
        },
        'parts': {
            'meta_title': 'Запчасти для мотоциклов - Купить запчасти | motolom24',
            'meta_description': 'Запчасти для мотоциклов всех марок. Двигатель, трансмиссия, тормоза. Оригинальные и аналоговые запчасти.',
            'meta_keywords': 'запчасти для мотоциклов, мотоциклетные запчасти, двигатель, трансмиссия, тормоза',
        },
        'accessories': {
            'meta_title': 'Аксессуары для мотоциклов - Шлемы, куртки, перчатки | motolom24',
            'meta_description': 'Аксессуары для мотоциклов: шлемы, куртки, перчатки, экипировка. Защита и комфорт для мотоциклистов.',
            'meta_keywords': 'аксессуары для мотоциклов, шлемы, куртки, перчатки, экипировка',
        },
        'sport': {
            'meta_title': 'Спортивные мотоциклы - Купить спортбайк | motolom24',
            'meta_description': 'Спортивные мотоциклы 600cc и 1000cc. Honda, Yamaha, Kawasaki. Высокие скорости и отличная управляемость.',
            'meta_keywords': 'спортивные мотоциклы, спортбайки, 600cc, 1000cc, Honda CBR, Yamaha R',
        },
        'cruiser': {
            'meta_title': 'Круизеры - Купить круизер | motolom24',
            'meta_description': 'Круизеры Harley-Davidson, Yamaha. Комфортные мотоциклы для дальних поездок. Классический стиль.',
            'meta_keywords': 'круизеры, Harley-Davidson, Yamaha V-Star, комфортные мотоциклы',
        },
        'enduro': {
            'meta_title': 'Эндуро мотоциклы - Купить эндуро | motolom24',
            'meta_description': 'Эндуро мотоциклы 250cc и 450cc. Honda CRF, Yamaha YZ. Для бездорожья и кросса.',
            'meta_keywords': 'эндуро мотоциклы, кроссовые мотоциклы, Honda CRF, Yamaha YZ, 250cc, 450cc',
        },
    }
    
    for slug, seo_data in categories_data.items():
        try:
            category = Category.objects.get(slug=slug)
            category.meta_title = seo_data['meta_title']
            category.meta_description = seo_data['meta_description']
            category.meta_keywords = seo_data['meta_keywords']
            category.save()
            print(f'Обновлена категория: {category.name}')
        except Category.DoesNotExist:
            print(f'Категория {slug} не найдена')
    
    # Обновляем статичные страницы
    pages_data = {
        'usloviya-i-dostavka': {
            'meta_title': 'Условия и доставка - motolom24',
            'meta_description': 'Условия покупки и доставки мотоциклов и запчастей. Кредит, рассрочка, бесплатная доставка по Москве.',
            'meta_keywords': 'условия покупки, доставка, кредит, рассрочка, мотоциклы',
        },
        'vykup-motociklov': {
            'meta_title': 'Выкуп мотоциклов - Продать мотоцикл | motolom24',
            'meta_description': 'Выкуп мотоциклов в любом состоянии. Быстрая оценка, наличный расчет, бесплатная эвакуация.',
            'meta_keywords': 'выкуп мотоциклов, продать мотоцикл, оценка мотоцикла, наличный расчет',
        },
        'kontakty': {
            'meta_title': 'Контакты - motolom24',
            'meta_description': 'Контакты магазина мотоциклов motolom24. Адрес, телефоны, режим работы. Москва, ул. Мотоциклетная.',
            'meta_keywords': 'контакты, адрес, телефоны, motolom24, мотоциклы Москва',
        },
    }
    
    for slug, seo_data in pages_data.items():
        try:
            page = StaticPage.objects.get(slug=slug)
            page.meta_title = seo_data['meta_title']
            page.meta_description = seo_data['meta_description']
            page.meta_keywords = seo_data['meta_keywords']
            page.save()
            print(f'Обновлена страница: {page.title}')
        except StaticPage.DoesNotExist:
            print(f'Страница {slug} не найдена')
    
    # Добавляем SEO к популярным товарам
    products_data = {
        'honda-cbr600rr': {
            'meta_title': 'Honda CBR600RR - Купить спортбайк | motolom24',
            'meta_description': 'Honda CBR600RR - спортивный мотоцикл 600cc. Мощность, управляемость, надежность. Гарантия, доставка.',
            'meta_keywords': 'Honda CBR600RR, спортбайк, 600cc, спортивный мотоцикл',
        },
        'yamaha-r1': {
            'meta_title': 'Yamaha R1 - Купить спортбайк 1000cc | motolom24',
            'meta_description': 'Yamaha R1 - легендарный спортбайк 1000cc. Максимальная мощность и технологии MotoGP.',
            'meta_keywords': 'Yamaha R1, спортбайк, 1000cc, MotoGP технологии',
        },
        'harley-davidson-sportster': {
            'meta_title': 'Harley-Davidson Sportster - Купить круизер | motolom24',
            'meta_description': 'Harley-Davidson Sportster - классический круизер. Американский стиль, комфорт, надежность.',
            'meta_keywords': 'Harley-Davidson Sportster, круизер, американский мотоцикл',
        },
    }
    
    for slug, seo_data in products_data.items():
        try:
            product = Product.objects.get(slug=slug)
            product.meta_title = seo_data['meta_title']
            product.meta_description = seo_data['meta_description']
            product.meta_keywords = seo_data['meta_keywords']
            product.save()
            print(f'Обновлен товар: {product.name}')
        except Product.DoesNotExist:
            print(f'Товар {slug} не найден')
    
    print('SEO-информация добавлена успешно!')


if __name__ == '__main__':
    add_seo_data() 