"""Модели для заказов (корзина реализуется в сессии)."""
from django.db import models


class Order(models.Model):
    """Модель заказа."""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('cancelled', 'Отменён'),
    ]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    name = models.CharField(max_length=100, verbose_name='Имя', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    items = models.TextField(
        verbose_name='Состав заказа'
    )  # JSON или строка

    class Meta:
        """Мета-класс для Order."""

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        """Строковое представление заказа."""
        return f'Заказ #{self.id} от {self.name}'

# Корзина будет реализована как класс в cart/cart.py, а не как модель
