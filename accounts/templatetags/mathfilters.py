from decimal import Decimal
from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    return Decimal(value) * Decimal(arg)
