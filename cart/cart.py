"""Класс корзины для работы через сессию."""
from shop.models import Product
from decimal import Decimal


class Cart:
    """Класс корзины, работающей через сессию."""

    def __init__(self, request):
        """Инициализация корзины из сессии пользователя."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавить товар в корзину или обновить его количество."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """Удалить товар из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session['cart'] = dict(self.cart)
            self.session.modified = True

    def clear(self):
        """Очистить корзину."""
        self.session['cart'] = {}
        self.save()

    def save(self):
        """Синхронизировать корзину с сессией и пометить сессию как изменённую."""
        self.session['cart'] = dict(self.cart)
        self.session.modified = True

    def __iter__(self):
        """Итерировать по товарам в корзине с объектами Product."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(product.id): product for product in products}
        for product_id, item in self.cart.items():
            product = products_map.get(product_id)
            if not product:
                continue
            yield {
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': Decimal(item['price']) * item['quantity'],
            }

    def __len__(self):
        """Получить общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Получить общую стоимость корзины."""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        ) 