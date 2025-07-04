"""
URL configuration for motolom24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from seo.admin import seo_admin_site
from media_manager.views import ckeditor_upload_create_mediafile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seo-admin/', seo_admin_site.urls),
    path('cart/', include('cart.urls')),
    path('', include('shop.urls')),
    path('', include('seo.urls')),
    re_path(r'^ckeditor/upload/', ckeditor_upload_create_mediafile, name='ckeditor_upload'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
