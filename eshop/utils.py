from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *

def sendReceipt(order, payment_status):
	items = OrderItem.objects.filter(order=order)

	context = {
		'order': order,
		'items': items,
		'payment_status': payment_status,
	}
	print("emailing")

	subject = 'Transaction Receipt'
	html_message = render_to_string('partials/receipt.html', context)
	plain_message = strip_tags(html_message)
	from_email = 'from@example.com'
	to = order.email

	mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)