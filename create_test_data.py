#!/usr/bin/env python
"""Скрипт для создания тестовых данных магазина motolom24."""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motolom24.settings')
django.setup()

from shop.models import Category, Product

def create_test_data():
    """Создать тестовые категории и товары."""
    
    # Удаляем существующие данные
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    # Создаем категории 1 уровня
    moto = Category.objects.create(name='Мотоциклы', slug='motorcycles')
    parts = Category.objects.create(name='Запчасти', slug='parts')
    accessories = Category.objects.create(name='Аксессуары', slug='accessories')
    
    # Создаем категории 2 уровня для мотоциклов
    sport = Category.objects.create(name='Спортивные', slug='sport', parent=moto)
    cruiser = Category.objects.create(name='Круизеры', slug='cruiser', parent=moto)
    enduro = Category.objects.create(name='Эндуро', slug='enduro', parent=moto)
    
    # Создаем категории 2 уровня для запчастей
    engine = Category.objects.create(name='Двигатель', slug='engine', parent=parts)
    transmission = Category.objects.create(name='Трансмиссия', slug='transmission', parent=parts)
    brakes = Category.objects.create(name='Тормоза', slug='brakes', parent=parts)
    
    # Создаем категории 3 уровня для спортивных мотоциклов
    sport_600 = Category.objects.create(name='600cc', slug='sport-600', parent=sport)
    sport_1000 = Category.objects.create(name='1000cc', slug='sport-1000', parent=sport)
    
    # Создаем категории 3 уровня для эндуро
    enduro_250 = Category.objects.create(name='250cc', slug='enduro-250', parent=enduro)
    enduro_450 = Category.objects.create(name='450cc', slug='enduro-450', parent=enduro)
    
    # Создаем товары
    products_data = [
        # Спортивные мотоциклы 600cc
        {'name': 'Honda CBR600RR', 'price': 450000, 'category': sport_600},
        {'name': 'Yamaha R6', 'price': 480000, 'category': sport_600},
        {'name': 'Kawasaki ZX-6R', 'price': 460000, 'category': sport_600},
        
        # Спортивные мотоциклы 1000cc
        {'name': 'Honda CBR1000RR', 'price': 850000, 'category': sport_1000},
        {'name': 'Yamaha R1', 'price': 880000, 'category': sport_1000},
        {'name': 'Kawasaki ZX-10R', 'price': 870000, 'category': sport_1000},
        
        # Круизеры
        {'name': 'Harley-Davidson Sportster', 'price': 650000, 'category': cruiser},
        {'name': 'Yamaha V-Star', 'price': 580000, 'category': cruiser},
        
        # Эндуро 250cc
        {'name': 'Honda CRF250R', 'price': 320000, 'category': enduro_250},
        {'name': 'Yamaha YZ250F', 'price': 340000, 'category': enduro_250},
        
        # Эндуро 450cc
        {'name': 'Honda CRF450R', 'price': 420000, 'category': enduro_450},
        {'name': 'Yamaha YZ450F', 'price': 440000, 'category': enduro_450},
        
        # Запчасти двигателя
        {'name': 'Поршень двигателя', 'price': 15000, 'category': engine},
        {'name': 'Кольца поршневые', 'price': 8000, 'category': engine},
        {'name': 'Клапаны', 'price': 12000, 'category': engine},
        
        # Запчасти трансмиссии
        {'name': 'Сцепление', 'price': 25000, 'category': transmission},
        {'name': 'Цепь', 'price': 5000, 'category': transmission},
        {'name': 'Звездочка', 'price': 3000, 'category': transmission},
        
        # Тормоза
        {'name': 'Тормозные колодки', 'price': 4000, 'category': brakes},
        {'name': 'Тормозной диск', 'price': 12000, 'category': brakes},
        
        # Аксессуары
        {'name': 'Шлем Arai', 'price': 45000, 'category': accessories},
        {'name': 'Куртка кожаная', 'price': 35000, 'category': accessories},
        {'name': 'Перчатки', 'price': 8000, 'category': accessories},
    ]
    
    for data in products_data:
        Product.objects.create(
            name=data['name'],
            slug=data['name'].lower().replace(' ', '-').replace('cc', 'cc'),
            price=data['price'],
            category=data['category'],
            description=f'Описание товара {data["name"]}',
            available=True
        )
    
    print('Тестовые данные созданы успешно!')
    print(f'Создано категорий: {Category.objects.count()}')
    print(f'Создано товаров: {Product.objects.count()}')

if __name__ == '__main__':
    create_test_data() 