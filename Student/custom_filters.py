# Create a custom template filter
from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dictionary, key):
    return dictionary.get(key, '')  # Return an empty string if key is not found
