"""Views для SEO-приложения."""
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import SEOSettings, SEOItem
from shop.models import Category, Product, StaticPage


def sitemap_xml(request):
    """Генерация sitemap.xml."""
    current_site = Site.objects.get_current()
    seo_settings = SEOSettings.get_settings()
    
    # Получаем все URL сайта
    urls = []
    
    # Главная страница
    urls.append({
        'loc': f'https://{current_site.domain}/',
        'lastmod': timezone.now().strftime('%Y-%m-%d'),
        'changefreq': 'daily',
        'priority': '1.0'
    })
    
    # Каталог
    urls.append({
        'loc': f'https://{current_site.domain}/catalog/',
        'lastmod': timezone.now().strftime('%Y-%m-%d'),
        'changefreq': 'weekly',
        'priority': '0.9'
    })
    
    # Категории
    for category in Category.objects.all():
        urls.append({
            'loc': f'https://{current_site.domain}/catalog/{category.slug}/',
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8'
        })
    
    # Товары
    for product in Product.objects.filter(available=True):
        urls.append({
            'loc': f'https://{current_site.domain}/product/{product.slug}/',
            'lastmod': product.updated.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.7'
        })
    
    # Статичные страницы
    for page in StaticPage.objects.filter(is_active=True):
        urls.append({
            'loc': f'https://{current_site.domain}/{page.slug}/',
            'lastmod': page.updated.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.6'
        })
    
    # Генерируем XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>{url["loc"]}</loc>\n'
        xml_content += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{url["priority"]}</priority>\n'
        xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    return HttpResponse(xml_content, content_type='application/xml')


def site_structure(request):
    """Отображение структуры сайта."""
    seo_settings = SEOSettings.get_settings()
    
    # Получаем структуру сайта
    structure = {
        'main_page': {
            'url': '/',
            'title': 'Главная страница',
            'seo': None
        },
        'catalog': {
            'url': '/catalog/',
            'title': 'Каталог',
            'seo': None,
            'categories': []
        },
        'static_pages': []
    }
    
    # Категории с вложенностью
    for category in Category.objects.filter(parent=None):
        cat_data = {
            'name': category.name,
            'url': f'/catalog/{category.slug}/',
            'seo': None,
            'children': []
        }
        
        # Подкатегории
        for subcat in category.children.all():
            subcat_data = {
                'name': subcat.name,
                'url': f'/catalog/{subcat.slug}/',
                'seo': None,
                'children': []
            }
            
            # Подподкатегории
            for subsubcat in subcat.children.all():
                subsubcat_data = {
                    'name': subsubcat.name,
                    'url': f'/catalog/{subsubcat.slug}/',
                    'seo': None
                }
                subcat_data['children'].append(subsubcat_data)
            
            cat_data['children'].append(subcat_data)
        
        structure['catalog']['categories'].append(cat_data)
    
    # Статичные страницы
    for page in StaticPage.objects.filter(is_active=True):
        page_data = {
            'name': page.title,
            'url': f'/{page.slug}/',
            'seo': None
        }
        structure['static_pages'].append(page_data)
    
    context = {
        'structure': structure,
        'seo_settings': seo_settings,
        'total_categories': Category.objects.count(),
        'total_products': Product.objects.filter(available=True).count(),
        'total_pages': StaticPage.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'seo/site_structure.html', context)


def robots_txt(request):
    """Генерация robots.txt."""
    seo_settings = SEOSettings.get_settings()
    
    if seo_settings.robots_txt:
        content = seo_settings.robots_txt
    else:
        # Стандартный robots.txt
        content = """User-agent: *
Allow: /

# Запрещаем админку
Disallow: /admin/
Disallow: /seo-admin/

# Разрешаем sitemap
Sitemap: https://motolom24.ru/sitemap.xml
"""
    
    return HttpResponse(content, content_type='text/plain')
