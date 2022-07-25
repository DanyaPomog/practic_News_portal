import code

from django import template
from news.models import Post
from django.template.defaultfilters import stringfilter


register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': '',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value} {postfix}'


@register.filter()
def censor(value):
    censor_list = ['boolshit', 'fucking', 'sucking'
                   'BOOLSHIT', 'FUCKING', 'SUCKING'
                   'Boolshit', 'Fucking', 'Sucking']
    for i in censor_list:
        if i.find(value):
            value = value.replace(i[3:5:], "*" * len(i))
    return f'{value}'
