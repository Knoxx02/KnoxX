from django import template
import re

register = template.Library()

@register.filter
def split(value, sep):
    """Return the string split by sep."""
    return value.split(sep)

@register.filter
def strip(value):
    """Return the string with leading and trailing whitespace removed."""
    return value.strip()

@register.filter
def get_item(list_obj, index):
    """Return item at specified index from list."""
    try:
        return list_obj[index]
    except:
        return ""