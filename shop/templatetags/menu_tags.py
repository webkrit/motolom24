import os
from django import template
from shop.models import MenuItem
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_menu():
    return MenuItem.objects.filter(is_active=True, parent=None).order_by('order', 'title')

@register.filter
def has_file(image_field):
    if not image_field:
        return False
    try:
        return os.path.isfile(image_field.path)
    except Exception:
        return False 