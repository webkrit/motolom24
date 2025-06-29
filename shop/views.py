"""View-функции для магазина motolom24."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

# Create your views here.

def index(request):
    """Главная страница: список всех товаров с пагинацией."""
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 12)  # 12 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/index.html', {'page_obj': page_obj})

def catalog(request, category_slug=None):
    """Каталог: категории и товары по выбранной категории (3 уровня вложенности)."""
    categories = Category.objects.filter(parent=None)
    category = None
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        # Получаем все дочерние категории (включая подкатегории)
        child_categories = category.children.all()
        grandchild_categories = []
        for child in child_categories:
            grandchild_categories.extend(child.children.all())
        
        # Фильтруем товары: из текущей категории + из всех дочерних + из всех внучатых
        products = products.filter(
            category__in=[category] + list(child_categories) + grandchild_categories
        )
    
    return render(
        request, 'shop/catalog.html', {
            'categories': categories,
            'category': category,
            'products': products,
        }
    )

def static_page(request, page):
    """Статичные страницы: условия, выкуп, контакты."""
    template_name = f'shop/static/{page}.html'
    return render(request, template_name)
