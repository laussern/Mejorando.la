# -*- coding: utf-8 -*-

import base64

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

# modelos de nuevo
from cursos.models import Curso, CursoRegistro, CursoDocente, CursoDia, CursoPago

#### ADMINISTRACION ####
# vista principal del administrador
@login_required(login_url='/edmin')
def admin(req):
	return render_to_response('edmin/index.html')

#### ADMINISTRACION DE CURSOS ####

# vista principal de cursos
@login_required(login_url='/edmin')
def curso(req):
	return render_to_response('edmin/curso/index.html', { 
		'cursos': Curso.objects.all(), 
		'docentes': CursoDocente.objects.all(),
		'alumnos': CursoRegistro.objects.all()
	})

# agregar un curso
@login_required(login_url='/edmin')
def curso_add(req):
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
			# carga de imagen
			uploaded_file = ContentFile(base64.b64decode(imagen.split(',')[1]))
			uploaded_file.name = imagen_n

			curso = Curso(nombre=nombre, slug=slug, pais=pais, precio=precio, descripcion=descripcion, direccion=direccion, info_pago=info_pago, mapa=mapa, imagen=uploaded_file)
			curso.save()
 
		 	return HttpResponse('OK')
		else: return HttpResponse('ERR')

	return render_to_response('edmin/curso/admin.html')

# editar un curso
@login_required(login_url='/edmin')
def curso_edit(req, curso_id):
	curso = get_object_or_404(Curso, id=curso_id)

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

	return render_to_response('edmin/curso/admin.html', { 'curso': curso})

# eliminar un curso
@login_required(login_url='/edmin')
def curso_delete(req, curso_id):
	return HttpResponse()


#### ADMINISTRACION DE DOCENTES ####

def jstatus_ok(vars):
	return simplejson.dumps({ 'status': 'ok', 'vars': vars })

def jstatus_err():
	return simplejson.dumps({ 'status': 'err' })

def serialize_docente(docente):
	return {
		'id': docente.id,
		'nombre': docente.nombre,
		'twitter': docente.twitter,
		'imagen': docente.get_imagen(),
		'tipo': 'docente'
	}

def serialize_dia(dia):
	return {
		'id': dia.id,
		'tema': dia.tema,
		'fecha': dia.fecha,
		'tipo': 'dia'
	}

# agregar un docente
@login_required(login_url='/edmin')
def docente_add(req, curso_id):
	curso = get_object_or_404(Curso, id=curso_id)

	if req.method == 'POST':
		nombre   = req.POST.get('nombre')
		twitter  = req.POST.get('twitter')
		perfil   = req.POST.get('perfil')
		imagen   = req.POST.get('imagen')
		imagen_n = req.POST.get('imagen_filename')

		if nombre and twitter and perfil and imagen and imagen_n:
			# carga de imagen
			uploaded_file = ContentFile(base64.b64decode(imagen.split(',')[1]))
			uploaded_file.name = imagen_n

			docente = CursoDocente(nombre=nombre, twitter=twitter, perfil=perfil, imagen=uploaded_file, curso=curso)

			docente.save()
 
			return HttpResponse(jstatus_ok(serialize_docente(docente)))
		else: return HttpResponse(jstatus_err())

	return render_to_response('edmin/docente/admin.html', { 'curso': curso  })

# editar un docente
@login_required(login_url='/edmin')
def docente_edit(req, docente_id):
	docente = get_object_or_404(CursoDocente, id=docente_id)

	if req.method == 'POST':
		nombre   = req.POST.get('nombre')
		twitter  = req.POST.get('twitter')
		perfil   = req.POST.get('perfil')
		imagen   = req.POST.get('imagen')
		imagen_n = req.POST.get('imagen_filename')

		if nombre and twitter and perfil:
			docente.nombre 	= nombre
			docente.twitter = twitter
			docente.perfil  = perfil

			if imagen and imagen_n:
				# carga de imagen
				uploaded_file = ContentFile(base64.b64decode(imagen.split(',')[1]))
				uploaded_file.name = imagen_n
				
				docente.imagen = uploaded_file

			docente.save()
 
			return HttpResponse(jstatus_ok(serialize_docente(docente)))
		else: return HttpResponse(jstatus_err())

	return render_to_response('edmin/docente/admin.html', { 'docente': docente})

# eliminar un docente
@login_required(login_url='/edmin')
def docente_delete(req, curso_id):
	return HttpResponse()

#### ADMINISTRACION DE DIAS ####

# agregar un dia
@login_required(login_url='/edmin')
def dia_add(req, curso_id):
	curso = get_object_or_404(Curso, id=curso_id)

	if req.method == 'POST':
		tema 	= req.POST.get('tema')
		fecha   = req.POST.get('fecha')
		temario = req.POST.get('temario')

		if tema and fecha and temario:
			dia = CursoDia(tema=tema, fecha=fecha, temario=temario, curso=curso)

			dia.save()

			return HttpResponse(jstatus_ok(serialize_dia(dia)))
		else: return HttpResponse(jstatus_err())

	return render_to_response('edmin/dia/admin.html', { 'curso': curso  })

# editar un dia
@login_required(login_url='/edmin')
def dia_edit(req, dia_id):
	dia = get_object_or_404(CursoDia, id=dia_id)

	if req.method == 'POST':
		tema 	= req.POST.get('tema')
		fecha   = req.POST.get('fecha')
		temario = req.POST.get('temario')

		if tema and fecha and temario:
			dia.tema 	= tema
			dia.fecha   = fecha
			dia.temario = temario

			dia.save()
 
			return HttpResponse(jstatus_ok(serialize_dia(dia)))
		else: return HttpResponse(jstatus_err())

	return render_to_response('edmin/dia/admin.html', { 'dia': dia})

# eliminar un dia
@login_required(login_url='/edmin')
def dia_delete(req, dia_id):
	return HttpResponse()


@login_required(login_url='/edmin')
def pago(req):
	return render_to_response('edmin/pago/index.html', {
		'cursos': Curso.objects.all()
	})


