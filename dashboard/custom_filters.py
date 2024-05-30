from django import template

register = template.Library()

@register.filter
def to(value, arg):
    return range(value, arg + 1)


@register.filter
def split_features(value):
    return value.split(',')