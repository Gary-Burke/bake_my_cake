from django import template

register = template.Library()


@register.filter
def friendly_label(value):
    return value.replace("_", " ").title()
