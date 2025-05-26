# templatetags/quiz_extras.py
from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    if not hasattr(obj, attr):
        return None
    return getattr(obj, attr)
