# templatetags/quiz_extras.py
from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    if not hasattr(obj, attr):
        return None
    return getattr(obj, attr)

from django import template
register = template.Library()

@register.filter
def dictkey(dict_data, key):
    return dict_data.get(key)
