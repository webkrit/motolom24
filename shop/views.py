"""View-функции для магазина motolom24."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category, StaticPage, Banner, MainPageSettings, FooterSettings, SiteSettings

# Create your views here.

def index(request):
    """Главная страница: слайдер баннеров, последние поступления, текстовый блок."""
    banners = Banner.objects.filter(is_active=True).order_by('order', '-created')
    main_settings = MainPageSettings.get_settings()
    products = Product.objects.filter(available=True).order_by('-created')[:main_settings.products_count]
    context = {
        'banners': banners,
        'products': products,
        'main_settings': main_settings,
        'meta_title': 'motolom24 - Интернет-магазин мотоциклов и запчастей',
        'meta_description': 'Купить мотоциклы, запчасти и аксессуары в интернет-магазине motolom24. Большой выбор, выгодные цены, доставка по России.',
        'meta_keywords': 'мотоциклы, запчасти, аксессуары, купить мотоцикл, мотоциклетные запчасти',
    }
    return render(request, 'shop/index.html', context)

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
    
    context = {
        'categories': categories,
        'category': category,
        'products': products,
    }
    
    # Добавляем SEO-информацию для категории
    if category:
        context.update({
            'meta_title': category.get_meta_title(),
            'meta_description': category.get_meta_description(),
            'meta_keywords': category.meta_keywords,
        })
    else:
        context.update({
            'meta_title': 'Каталог - motolom24',
            'meta_description': 'Каталог мотоциклов, запчастей и аксессуаров. Выберите нужную категорию.',
            'meta_keywords': 'каталог мотоциклов, категории, запчасти, аксессуары',
        })
    
    return render(request, 'shop/catalog.html', context)

def static_page(request, page_slug):
    """Статичные страницы из базы данных."""
    page = get_object_or_404(StaticPage, slug=page_slug, is_active=True)
    
    context = {
        'page': page,
        'meta_title': page.get_meta_title(),
        'meta_description': page.get_meta_description(),
        'meta_keywords': page.meta_keywords,
    }
    
    return render(request, 'shop/static_page.html', context)

def footer_settings(request):
    return {'footer_settings': FooterSettings.get_settings()}

def site_settings(request):
    return {'site_settings': SiteSettings.get_settings()}

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    meta_title = product.get_meta_title()
    meta_description = product.get_meta_description()
    meta_keywords = product.meta_keywords
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })
