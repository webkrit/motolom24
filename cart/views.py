"""Views для корзины и оформления заказа."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .models import Order
from django.conf import settings
from django.core.mail import send_mail
import json
from django.contrib import messages

# Create your views here.

@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if not product.available or product.quantity < 1:
        messages.error(request, f'Товар "{product.name}" недоступен для заказа.')
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    quantity = int(request.POST.get('quantity', 1))
    product_id_str = str(product.id)
    in_cart = cart.cart.get(product_id_str, {}).get('quantity', 0)
    if product.quantity < in_cart + quantity:
        messages.error(
            request,
            f'Нельзя добавить больше {product.quantity} шт. товара "{product.name}" в корзину.'
        )
        return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))
    cart.add(product=product, quantity=quantity, update_quantity=False)
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))

# @require_POST
def cart_remove(request, product_id):
    """Удалить товар из корзины."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_clear(request):
    """Очистить корзину."""
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

def cart_detail(request):
    """Показать содержимое корзины и обработать обновление количества."""
    cart = Cart(request)
    if request.method == 'POST':
        updated = False
        # Собираем id товаров из корзины
        for item in cart:
            product = item['product']
            field = f'quantity_{product.id}'
            if field in request.POST:
                try:
                    qty = int(request.POST[field])
                except Exception:
                    qty = 1
                if qty < 1:
                    qty = 1
                if qty > product.quantity:
                    qty = product.quantity
                cart.add(product=product, quantity=qty, update_quantity=True)
                updated = True
        if updated:
            messages.success(request, 'Корзина обновлена.')
        return redirect('cart_detail')
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def order_create(request):
    """Оформить заказ (GET — форма, POST — обработка)."""
    cart = Cart(request)
    if not len(cart):
        return redirect('cart_detail')
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        if not phone:
            messages.error(request, 'Пожалуйста, укажите телефон.')
            return render(request, 'cart/order_form.html', {'cart': cart})
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()
        items = [
            {
                'product_id': item['product'].id,
                'name': item['product'].name,
                'price': str(item['product'].price),
                'quantity': item['quantity'],
            }
            for item in cart
        ]
        # Проверка и уменьшение остатков
        for item in cart:
            product = item['product']
            if product.quantity < item['quantity']:
                messages.error(request, f'Недостаточно товара "{product.name}" на складе.')
                return redirect('cart_detail')
        for item in cart:
            product = item['product']
            product.quantity -= item['quantity']
            if product.quantity < 1:
                product.available = False
            product.save()
        order = Order.objects.create(
            name=name,
            email='',
            phone=phone,
            address=address,
            comment=comment,
            items=json.dumps(items, ensure_ascii=False)
        )
        # Отправка письма
        order_email = getattr(settings, 'ORDER_EMAIL', None)
        if order_email:
            subject = f'Новый заказ #{order.id}'
            message = (
                f'Телефон: {phone}\nИмя: {name}\nАдрес: {address}\n'
                f'Комментарий: {comment}\n\nСостав заказа:\n'
            )
            for item in items:
                message += f"- {item['name']} x {item['quantity']} = {item['price']}\n"
            message += f"\nИтого: {cart.get_total_price()} руб."
            send_mail(subject, message, order_email, [order_email])
        cart.clear()
        return render(request, 'cart/order_success.html', {'order': order})
    return render(request, 'cart/order_form.html', {'cart': cart})
