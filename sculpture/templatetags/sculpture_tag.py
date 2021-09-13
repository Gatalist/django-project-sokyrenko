from django import template
from sculpture.models import Category, Sculpture

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()
