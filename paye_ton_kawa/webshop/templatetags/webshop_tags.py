# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/
from django import template
from django.template import Variable, VariableDoesNotExist

register = template.Library()


# https://stackoverflow.com/a/3466349
@register.filter
def attr(obj, att):
    pseudo_context = {'object': obj}
    try:
        value = Variable('object.%s' % att).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None

    return value
