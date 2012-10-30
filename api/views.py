# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from website.models import Video, VideoComentario, Curso
from django.core import serializers


# el archivo de cursos 
# organizados por mes-año
def cursos(solicitud):
    return HttpResponse(serializers.serialize('json', Curso.objects.filter(activado=True)), mimetype='application/json')
    
# el archivo muestra todos los videos
# organizados por mes-año
def videos(solicitud):
    return HttpResponse(serializers.serialize('json', Video.objects.filter(activado=True)), mimetype='application/json')
