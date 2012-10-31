# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.conf import settings

from models import Curso, CursoRegistro
from website.utils import get_pais

import stripe

stripe.api_key = settings.STRIPE_API_KEY

def send_mail(tipo, vs, subject, email):
	html_content = render_to_string('nuevo/email/%s.html' % tipo, vs)
	mail = EmailMultiAlternatives(subject,
		strip_tags(html_content), 'Cursos Mejorando.la <ventas@mejorando.la>', [email])

	mail.attach_alternative(html_content, 'text/html')
	mail.send()

# vista publica del curso
def curso(req, curso_slug):
	curso = get_object_or_404(Curso, slug=curso_slug)
	vs 	  = { 'curso': curso } # variables para el rendereo de la plantilla

	if req.method == 'POST':
		nombre = req.POST.get('nombre')
		email  = req.POST.get('email')
		tel    = req.POST.get('telefono')
		method = req.POST.get('method')

		if nombre and email and tel:
			# buscar si el usuario ya existe en la bd
			try: 
				registro = CursoRegistro.objects.get(email=req.POST)
			# si no existe crearlo
			except CursoRegistro.DoesNotExist:
				registro = CursoRegistro(nombre=nombre, email=email, telefono=telefono, pais=get_pais(req.META))
				registro.save()


			# agregar el curso a los registro de usuario
			registro.curso.add(curso)

			# pagar por el curso
			if  method == 'tarjeta':
				token = req.POST.get('stripeToken')

				# checar que venga el token de stripe
				if not token: return HttpResponse('ERR')

				# realizar el cargo con la api de stripe
				charge = stripe.Charge.create(
					amount		= curso.precio,
					currency	= 'usd',
					card	    = token,
					description = email
				)

				# si se realiza el cargo con exito enviar mail de confirmacion de pago
				if charge.paid: 
					# agregar como curso pagado
					registro.pagado.add(curso)

					send_mail('curso_pago', vs, 'Confirmacion de pago | %s' % curso.nombre, email)
				else: return HttpResponse('ERR')

			# mandar los datos para registro con deposito
			else:
				send_mail('curso_info', vs, 'Informacion para pago | %s' % curso.nombre, email)

			return HttpResponse('OK')

		else: return HttpResponse('ERR')
	
	return render_to_response('nuevo/curso.html', vs)


