# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from website.models import Video, VideoComentario, Curso



# el archivo de cursos 
# organizados por mes-año
def cursos(solicitud):
	return HttpResponse(simplejson.dumps({'meses': [{
			'fecha' : fecha,
			'cursos': Curso.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, activado=True).order_by('-fecha')
		} for fecha in Curso.objects.filter(activado=True).dates('fecha', 'month', order='DESC')]
	}))

# el archivo muestra todos los videos
# organizados por mes-año
def videos(solicitud):
	return HttpResponse(simplejson.dumps({'meses': [{
            'fecha': fecha,
            'videos': Video.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, activado=True).order_by('-fecha')
        } for fecha in Video.objects.filter(activado=True).dates('fecha', 'month', order='DESC')]
   }))


# la entrada de video muestra el video
# del capitulo + comentarios + formulario de comentarios
# tambien procesa +1 comentario
def video(solicitud, video_slug):
    # video por slug (nombre)
    video = get_object_or_404(Video, slug=video_slug)
    comentarios = VideoComentario.objects.filter(video_id=video.id).order_by('-fecha', '-id')

    return HttpResponse(simplejson.dumps({
        'video': video,  # datos del video particular
        'comentarios': comentarios  # comentarios al video
    }))
