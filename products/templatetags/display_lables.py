from django import template

register = template.Library()


@register.filter
def friendly_label(value):
    return value.replace("_", " ").title()


@register.filter
def get_item(dictionary, key):
    return str(dictionary.get(key, ""))
