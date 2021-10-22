from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(d, key):
	try:
		t = d[key]
	except:
		return None

	return t
