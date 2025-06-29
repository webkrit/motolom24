from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:category_slug>/', views.catalog, name='category_detail'),
    path('conditions/', views.static_page, {'page': 'conditions'}, name='conditions'),
    path('buyout/', views.static_page, {'page': 'buyout'}, name='buyout'),
    path('contacts/', views.static_page, {'page': 'contacts'}, name='contacts'),
] 