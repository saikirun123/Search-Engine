from django import template

register = template.Library()

@register.filter(name='return_a_list')
def return_a_list(argument):
    if isinstance(argument, list):
        return range(len(argument))
    else :
        pass

@register.filter(name='dictionary_lookup')
def dictionary_lookup(var,arg):
    if isinstance(arg, dict):
        return arg[var]
    else :
        pass
