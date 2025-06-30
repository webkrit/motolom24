from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:category_slug>/', views.catalog, name='category_detail'),
    path('<slug:page_slug>/', views.static_page, name='static_page'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
] 