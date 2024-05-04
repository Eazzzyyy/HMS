from django import template

register = template.Library()

@register.filter
def split_features(features):
    return features.split(', ')
