from django import template
import locale
locale.setlocale(locale.LC_ALL, '')

register = template.Library()

@register.simple_tag
def getsubtotal (quantity, price):
	subtotal = quantity * price
	string_subtotal = '%.2f' % float(subtotal)
	return f'{float(string_subtotal):n}'
	# return string_subtotal