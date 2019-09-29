import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)

def to_class_name(value):
    return value.__class__.__name__

register.filter('to_class_name', to_class_name)

def to_model_name(value):        
    try:
        model = value.model.__name__
    except:
        model = value.Meta.model.__name__

    return model

register.filter('to_model_name', to_model_name)