__author__ = 'Tadej'

from django import template

register = template.Library()

@register.filter()
def custom_range(value):
    return range(value)

@register.filter()
def wrap_int_in_list(value):
    if type(value) is int:
        return [value]
    if type(value) is list:
        return value
    return None