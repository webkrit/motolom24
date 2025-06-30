from django.contrib import admin
from .models import Order
import json

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'order_items_pretty', 'status', 'created')
    list_filter = ('created', 'status')
    search_fields = ('name', 'phone', 'address', 'comment')
    readonly_fields = ('created', 'items', 'order_items_pretty')
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'address', 'comment', 'order_items_pretty', 'status', 'created')
        }),
    )
    actions = ['confirm_orders', 'cancel_orders']

    def order_items_pretty(self, obj):
        try:
            items = json.loads(obj.items)
        except Exception:
            return obj.items
        html = '<ul>'
        for item in items:
            html += f'<li>{item["name"]} — {item["quantity"]} x {item["price"]} ₽</li>'
        html += '</ul>'
        return html
    order_items_pretty.short_description = 'Состав заказа'
    order_items_pretty.allow_tags = True

    @admin.action(description='Подтвердить выбранные заказы')
    def confirm_orders(self, request, queryset):
        from shop.models import Product
        for order in queryset.filter(status='new'):
            items = json.loads(order.items)
            for item in items:
                try:
                    product = Product.objects.get(id=item['product_id'])
                    product.quantity -= item['quantity']
                    if product.quantity < 1:
                        product.available = False
                    product.save()
                except Product.DoesNotExist:
                    continue
            order.status = 'confirmed'
            order.save()
        self.message_user(request, 'Выбранные заказы подтверждены, остатки обновлены.')

    @admin.action(description='Отменить выбранные заказы')
    def cancel_orders(self, request, queryset):
        """Отменяет выбранные заказы и возвращает товары в каталог, если они были списаны."""
        from shop.models import Product
        count = 0
        for order in queryset:
            if order.status != 'cancelled':
                items = json.loads(order.items)
                for item in items:
                    try:
                        product = Product.objects.get(id=item['product_id'])
                        product.quantity += item['quantity']
                        product.available = True
                        product.save()
                    except Product.DoesNotExist:
                        continue
                order.status = 'cancelled'
                order.save()
                count += 1
        self.message_user(
            request,
            (
                f'Отменено заказов: {count}, '
                'товары возвращены в каталог.'
            )
        )
