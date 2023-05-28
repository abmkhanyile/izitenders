from django import template

register = template.Library()

@register.filter(name='html_formatter')
def html_formatter(textToformat, arg=0):
    pass
