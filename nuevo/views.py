# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from models import Curso
from django.http import HttpResponse

def curso(req, curso_slug):
	curso = get_object_or_404(Curso, slug=curso_slug)

	if req.method == 'POST':
		
		if req.POST.get('nombre') and req.POST.get('email'):
			html_content = render_to_string('nuevo/email/curso_pago.html', { 'curso': curso })
			mail = EmailMultiAlternatives('Confirmacion de pago | %s' % curso.nombre,
			 	strip_tags(html_content), 'Adan Sanchez <adan@mejorando.la>', [req.POST.get('email')])

			mail.attach_alternative(html_content, 'text/html')
			mail.send()

		return HttpResponse('OK')
	
	return render_to_response('nuevo/curso.html', { 'curso': curso })