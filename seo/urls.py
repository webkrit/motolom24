from django.urls import path
from . import views

app_name = 'seo'

urlpatterns = [
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('structure/', views.site_structure, name='site_structure'),
] 