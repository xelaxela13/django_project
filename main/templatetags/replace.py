from django import template

register = template.Library()


@register.filter(name='cut')
def replace_char_in_the_string(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
