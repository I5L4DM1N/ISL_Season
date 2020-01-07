from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtratcs value from original value"""
    return_value = value - arg
    return return_value


@register.filter
def add(value, arg):
    """Subtratcs value from original value"""
    return_value = value + arg
    return return_value

@register.filter
def multiply(value, arg):
    """Subtratcs value from original value"""
    return_value = value * arg
    return return_value
