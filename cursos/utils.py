# -*- coding: utf-8 -*-

import math

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def send_mail(tipo, vs, subject, email):
	html_content = render_to_string('cursos/email/%s.html' % tipo, vs)
	mail = EmailMultiAlternatives(subject,
		strip_tags(html_content), 'Cursos Mejorando.la <ventas@mejorando.la>', [email])

	mail.attach_alternative(html_content, 'text/html')
	mail.send()


def calculate(quantity, price):
	rate  = math.floor( quantity / 5 )
	total = price * quantity

	# descuento de plazas gratis
	discount = rate * price

	# aplicar el descuento solo cuando no sea cada 5 (que es cuando hay una plaza gratis mas)
	if (quantity % 5) != 0:
		discount += (price * 0.1) * (quantity-1 if quantity < 5 else quantity - (5 * rate) )

	return {
		'amount'   : int(total - discount),
		'total'	   : int(total),
		'discount' : int(discount)
	}