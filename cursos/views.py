# -*- coding: utf-8 -*-
import math

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404
from django.template import TemplateDoesNotExist, RequestContext

from models import Curso, CursoRegistro, CursoPago
from website.utils import get_pais
from utils import send_mail

import stripe
import requests

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(req):
	import website.models

	# el archivo de cursos 
	# organizados por mes-año
	return render_to_response('cursos/home.html', {
		'meses': [{
			'fecha' : fecha,
			'cursos': website.models.Curso.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, activado=True).order_by('-fecha')
		} for fecha in website.models.Curso.objects.filter(activado=True).dates('fecha', 'month', order='DESC')]
	})


# vista publica del curso
def curso(req, curso_slug):
	if req.method == 'POST':
		curso = get_object_or_404(Curso, slug=curso_slug)
		vs 	  = { 'curso': curso } # variables para el rendereo de la plantilla

		action = req.POST.get('action')

		if action:
			if action == 'buy':
				nombre 	 = req.POST.get('nombre')
				email  	 = req.POST.get('email')
				tel    	 = req.POST.get('telefono')
				quantity = req.POST.get('quantity')
				token 	 = req.POST.get('stripeToken')

				if nombre and email and tel and quantity and token:
					quantity = int(quantity)

					rate  = math.floor( quantity / 5 )
					total = curso.precio * quantity

					# descuento de plazas gratis
					discount = rate * curso.precio

					#aplicar el descuento solo cuando no sea cada 5 (que es cuando hay una plaza gratis mas)
					if (quantity % 5) != 0:
						discount += (curso.precio * 0.1) * (quantity-1 if quantity < 5 else quantity - (5 * rate) )

					amount = total - discount

					# realizar el cargo con la api de stripe
					try:
						charge = stripe.Charge.create(
							amount		= int(amount),
							currency	= 'usd',
							card	    = token,
							description = email
						)
					except Exception: return HttpResponse('ERR')

					# si se realiza el cargo con exito enviar mail de confirmacion de pago
					if not charge.paid: return HttpResponse('ERR')

					p = CursoPago(nombre=nombre, email=email, telefono=tel, pais=get_pais(req.META), quantity=quantity, curso=curso)
					p.save()

					req.session['p32'] = p.id

					vs['amount']   = amount
					vs['discount'] = discount
					vs['total']    = total
					vs['pago']     = p

					send_mail('curso_pago', vs, 'Gracias por tu pago al %s de Mejorando.la INC' % curso.nombre, email)

					return HttpResponse('OK')

				else: return HttpResponse('ERR')

			elif action == 'register':
				email = req.POST.getlist('email')
				pago  = req.session.get('p32')

				if email and pago:
					p = get_object_or_404(CursoPago, id=pago)


					for e in email:
						r = CursoRegistro(email=e, pago=p)
						r.save()

						# integracion con la plataforma
						try:
							r = requests.post(u'%spreregistro' % settings.PLATAFORMA_API_URL, { 'slug': curso.slug, 'email': e, 'passwd': settings.PLATAFORMA_API_KEY })
						except: return HttpResponse('ERR')

					return HttpResponse('OK')
					
				else: return HttpResponse('ERR')

			else: return HttpResponse('ERR')
		else: return HttpResponse('ERR')

	try:
		curso = Curso.objects.get(slug=curso_slug)
	except Curso.DoesNotExist: curso = None

	vs = RequestContext(req, { 'curso': curso, 'publishable_key': settings.STRIPE_PUBLISHABLE_KEY })
	try:
		return render_to_response('%s.html' % curso_slug, vs)
	except TemplateDoesNotExist:
		if not curso: raise Http404

		return render_to_response('cursos/curso.html', vs)

