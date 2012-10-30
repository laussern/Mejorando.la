# -*- coding: utf-8 -*-

import base64

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

from models import Curso, CursoRegistro, CursoDocente
from website.utils import get_pais

import stripe

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


@login_required(login_url='/nuevo/admin')
def admin(req):
	return render_to_response('nuevo/admin.html', { 
		'cursos': Curso.objects.all(), 
		'docentes': CursoDocente.objects.all(),
		'alumnos': CursoRegistro.objects.all()
	})

@login_required(login_url='/nuevo/admin')
def admin_add(req):
	if req.method == 'POST':
		nombre 		= req.POST.get('nombre')
		slug   		= req.POST.get('slug')
		pais   		= req.POST.get('pais')
		precio   	= req.POST.get('precio')
		descripcion = req.POST.get('descripcion')
		direccion   = req.POST.get('direccion')
		mapa    	= req.POST.get('mapa')
		imagen		= req.POST.get('imagen')
		imagen_n    = req.POST.get('imagen_filename')
		info_pago   = req.POST.get('info_pago')

		if nombre and slug and pais and precio and descripcion and direccion and mapa and info_pago and imagen and imagen_n:
			curso = Curso(nombre=nombre, slug=slug, pais=pais, precio=precio, descripcion=descripcion, direccion=direccion, info_pago=info_pago, mapa=mapa)

			# carga de imagen
			uploaded_file = ContentFile(base64.b64decode(imagen.split(',')[1]))
			uploaded_file.name = imagen_n
			
			curso.imagen = uploaded_file

			curso.save()
 
		 	return HttpResponse('OK')
		else: return HttpResponse('ERR')

	return render_to_response('nuevo/admin_add.html')

@login_required(login_url='/nuevo/admin')
def admin_edit(req, curso_slug):
	curso = get_object_or_404(Curso, slug=curso_slug)

	if req.method == 'POST':
		nombre 		= req.POST.get('nombre')
		slug   		= req.POST.get('slug')
		pais   		= req.POST.get('pais')
		precio   	= req.POST.get('precio')
		descripcion = req.POST.get('descripcion')
		direccion   = req.POST.get('direccion')
		mapa    	= req.POST.get('mapa')
		imagen		= req.POST.get('imagen')
		imagen_n    = req.POST.get('imagen_filename')
		info_pago   = req.POST.get('info_pago')

		if nombre and slug and pais and precio and descripcion and direccion and mapa and info_pago:
			curso.nombre 	  = nombre
			curso.slug  	  = slug
			curso.pais 		  = pais
			curso.precio 	  = precio
			curso.descripcion = descripcion
			curso.direccion   = direccion
			curso.mapa 		  = mapa
			curso.info_pago   = info_pago

			if imagen and imagen_n:
				# carga de imagen
				uploaded_file = ContentFile(base64.b64decode(imagen.split(',')[1]))
				uploaded_file.name = imagen_n
				
				curso.imagen = uploaded_file

			curso.save()
 
			return HttpResponse('OK')
		else: return HttpResponse('ERR')

	return render_to_response('nuevo/admin_add.html', { 'curso': curso})

@login_required(login_url='/nuevo/admin')
def admin_delete(req, curso_slug):
	return HttpResponse()