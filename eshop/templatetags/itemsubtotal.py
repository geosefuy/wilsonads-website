from django import template

register = template.Library()

@register.simple_tag
def getsubtotal (quantity, price):
	subtotal = quantity * price
	string_subtotal = '%.2f' % float(subtotal)
	return string_subtotal