import importlib

from django import template
register = template.Library()

# takes a model and returns the entry with given id
# example usage: a thread retrieving its author by id
@register.simple_tag
def resolve(id, package, model):
	m = importlib.import_module(package + '.models')
	c = getattr(m, model)
	return c.objects.get(id=id)
