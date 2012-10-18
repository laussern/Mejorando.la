# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from models import Curso, CursoRegistro
from django.http import HttpResponse
from django.conf import settings
import stripe
from website.utils import get_pais

stripe.api_key = settings.STRIPE_API_KEY

def curso(req, curso_slug):
	curso = get_object_or_404(Curso, slug=curso_slug)

	if req.method == 'POST':
	
		if req.POST.get('nombre') and req.POST.get('email') and req.POST.get('telefono'):
			registro = CursoRegistro(nombre=req.POST.get('nombre'), email=req.POST.get('email'), telefono=req.POST.get('telefono'), pais=get_pais(req.META))
			registro.save()

			if req.POST.get('method') == 'tarjeta':
				if not req.POST.get('stripeToken'): return HttpResponse('ERR')

				charge = stripe.Charge.create(
					amount=curso.precio,
					currency='usd',
					card=req.POST.get('stripeToken'),
					description=req.POST.get('email')
				)

				if charge.paid: 
					registro.pagado = True
					registro.save()

					html_content = render_to_string('nuevo/email/curso_pago.html', { 'curso': curso })
					mail = EmailMultiAlternatives('Confirmacion de pago | %s' % curso.nombre,
						strip_tags(html_content), 'Cursos Mejorando.la <ventas@mejorando.la>', [req.POST.get('email')])

					mail.attach_alternative(html_content, 'text/html')
					mail.send()
				else: return HttpResponse('ERR')

			elif req.POST.get('method') == 'deposito':

				html_content = render_to_string('nuevo/email/curso_info.html', { 'curso': curso })
				mail = EmailMultiAlternatives('Informacion para pago | %s' % curso.nombre,
					strip_tags(html_content), 'Cursos Mejorando.la <ventas@mejorando.la>', [req.POST.get('email')])

				mail.attach_alternative(html_content, 'text/html')
				mail.send()


			return HttpResponse('OK')
	
	return render_to_response('nuevo/curso.html', { 'curso': curso })