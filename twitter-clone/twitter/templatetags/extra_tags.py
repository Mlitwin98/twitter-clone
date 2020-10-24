from django import template
from django.db.models import Count

register = template.Library()

@register.filter
def get_value_in_qs(queryset, key):
    return queryset.values_list(key, flat=True)

@register.simple_tag
def count_values_in_qs(queryset, key, value):
    count = queryset.filter(**{key:value}).annotate(cnt=Count(key))
    return count[0].cnt