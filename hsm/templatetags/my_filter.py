from django import template

register = template.Library()


@register.filter(name='create_range')
def create_range(value, start_index=0):
    return range(start_index, value + start_index)