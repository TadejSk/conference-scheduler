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

@register.filter()
def allign_schedule(value):
    l = wrap_int_in_list(value)
    ln = int(12/len(l))
    if ln < 4:
        ln = 4
    return ln

@register.filter()
def mul(value, arg):
    return value*arg

@register.filter()
def div(value, arg):
    return int(value/arg)

@register.filter()
def get_element_at(value, arg):
    return value[arg]

@register.filter()
def multiarg_get_element_at(value, arg):
    args = [int(a.split(",").strip() for a in arg)]
    element = value
    for arg in args():
        element = value[arg]
    return element

@register.filter()
def mod(value, arg):
    return value % arg