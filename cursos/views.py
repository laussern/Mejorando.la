# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404
from django.template import TemplateDoesNotExist

from models import Curso, CursoRegistro
from website.utils import get_pais
from utils import send_mail

import stripe

stripe.api_key = settings.STRIPE_API_KEY

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
	try:
		curso = Curso.objects.get(slug=curso_slug)
	except Curso.DoesNotExist:
		try:
			return render_to_response('%s.html' % curso_slug)
		except TemplateDoesNotExist: raise Http404
		
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
	
	return render_to_response('cursos/curso.html', vs)


