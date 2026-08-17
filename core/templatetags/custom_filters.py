# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def add(value, arg):
    return value + arg


@register.filter
def absolute(value):
    return abs(value)


@register.filter
def add_commas(value):
    """Add commas to an integer or float value."""
    if isinstance(value, (int, float)):
        return "{:,.2f}".format(value)  # Formats with two decimal places
    return value