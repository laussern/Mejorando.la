# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core import serializers
from django.core.mail import send_mail
from django.utils import simplejson
from django.template import TemplateDoesNotExist
from django.template.defaultfilters import slugify
from akismet import Akismet
import image
from models import Setting, Video, VideoComentario, VideoComentarioForm, Curso, RegistroCurso, RegistroConferencia, Conferencia
import datetime
import time
import requests
import urllib
from utils import get_pais


# La vista del home muestra el ultimo video destacado
# y 4 videos mas, + el horario localizado
def home(solicitud):
    # si no existe el valor aun en la base de datos
    try:
        es_vivo = Setting.objects.get(key='en_vivo').value
    except Setting.DoesNotExist:
        es_vivo = False

    # checar si estamos transmitiendo en vivo
    # regresar la vista de "vivo" de ser asi
    if ('live' in solicitud.GET and solicitud.GET['live'] == '1') or es_vivo:
        return render_to_response('website/live.html')

    # si no hay videos aun
    try:
        ultimo_video = Video.objects.all().filter(activado=True).latest('fecha')
    except Video.DoesNotExist:
        ultimo_video = None

    ultimos_4_videos = Video.objects.all().order_by('-fecha').filter(activado=True)[1:5]
    # plantilla
    return render_to_response('website/home.html', {
        'ultimo_video': ultimo_video,  # El ultimo video
        'videos': ultimos_4_videos,  # ultimos 4 videos
        'pais': get_pais(solicitud.META),  # el horario del programa localizado
        'timestamp': get_timestamp(),  # Obtiene el timestamp del sig. program.
        'cursos': Curso.objects.all().order_by('fecha').filter(activado=True, fecha__gte=datetime.datetime.now()),
        'cursos_geo': Curso.objects.all().order_by('fecha').filter(activado=True, fecha__gte=datetime.datetime.now(), pais=get_pais(solicitud.META))
    })


def siguiente_jueves_4pm(now):
    _4PM = datetime.time(hour=13)
    _JUE = 3  # Monday=0 for weekday()
    old_now = now
    now += datetime.timedelta((_JUE - now.weekday()) % 7)
    now = now.combine(now.date(), _4PM)
    if old_now >= now:
        now += datetime.timedelta(days=7)
    return now


def get_timestamp():
    now = datetime.datetime.now()
    sig_jueves = siguiente_jueves_4pm(now)
    return int(time.mktime(sig_jueves.timetuple()) * 1000)


# el archivo muestra todos los videos
# organizados por mes-año
def videos(solicitud):
    return render_to_response('website/videos.html', {
        'meses': [{
            'fecha': fecha,
            'videos': Video.objects.filter(fecha__year=fecha.year,
                                        fecha__month=fecha.month, activado=True).order_by('-fecha')
        } for fecha in Video.objects.filter(activado=True).dates('fecha', 'month', order='DESC')]
    })


def conferencias(solicitud):
    return render_to_response('website/conferencias.html', {
        'meses': [{
            'fecha' : fecha,
            'confes': Conferencia.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, activado=True).order_by('-fecha')
        } for fecha in Conferencia.objects.filter(activado=True).dates('fecha', 'month', order='DESC')]
    })

# la entrada de video muestra el video
# del capitulo + comentarios + formulario de comentarios
# tambien procesa +1 comentario
def video(solicitud, video_slug):
    # video por slug (nombre)
    video = get_object_or_404(Video, slug=video_slug)

    # si son datos del formulario de comentarios
    if solicitud.method == 'POST':
        form = VideoComentarioForm(solicitud.POST)

        # validar los datos
        if(form.is_valid()):
            # asignar el video
            comentario = form.save(commit=False)
            comentario.video = video

            # detectar spam
            api = Akismet(key=settings.AKISMET_API_KEY,
                        blog_url=settings.AKISMET_URL,
                        agent=settings.AKISMET_AGENT)
            if api.verify_key():
                # por si el usuario esta detras de un proxy
                if 'HTTP_X_FORWARDED_FOR' in solicitud.META and solicitud.META['HTTP_X_FORWARDED_FOR']:
                    ip = solicitud.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
                else:
                    ip = solicitud.META['REMOTE_ADDR']

                if not api.comment_check(comment=comentario.content, data={
                        'user_ip': ip,
                        'user_agent': solicitud.META['HTTP_USER_AGENT']
                    }):

                    # guardar el video
                    comentario.save()
    else:
        form = VideoComentarioForm()

    comentarios = VideoComentario.objects.filter(video_id=video.id).\
                                            order_by('-fecha', '-id')
    return render_to_response('website/video.html', {
        'video': video,  # datos del video particular
        'form': form,  # formulario de comentarios
        'comentarios': comentarios  # comentarios al video
    })


# plantilla de transmision en vivo
def live(solicitud):
    return render_to_response('website/live.html')


# volver a generar las imagenes de video
# en todos sus sizes
@login_required()
def regenerate(solicitud):
    for video in Video.objects.all():
        image.resize(image.THUMB, video.imagen)
        image.resize(image.SINGLE, video.imagen)
        image.resize(image.HOME, video.imagen)

    for curso in Curso.objects.all():
        image.resize(image.THUMB, curso.imagen)

    return redirect('/')


def handler404(solicitud):
    return redirect('website.views.home')


from django.http import HttpResponse

def locateme(solicitud):
    return HttpResponse(get_pais(solicitud.META))

def hola(solicitud):

    if solicitud.method == 'POST' and solicitud.POST.get('email') and solicitud.POST.get('nombre'):
        pais   = get_pais(solicitud.META)
        email  = solicitud.POST['email']
        nombre = solicitud.POST['nombre']

        # por si el usuario esta detras de un proxy
        if solicitud.META.get('HTTP_X_FORWARDED_FOR'):
            ip = solicitud.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
        else:
            ip = solicitud.META['REMOTE_ADDR']

        payload = {
            'email_address': email,
            'apikey': settings.MAILCHIMP_APIKEY,
            'merge_vars': {
                'FNAME': nombre,
                'OPTINIP': ip,
                'OPTIN_TIME': time.time(),
                'PAIS': pais
            },
            'id': settings.MAILCHIMP_LISTID,
            'email_type': 'html'
        }

        r = requests.post('http://us2.api.mailchimp.com/1.3/?method=listSubscribe', simplejson.dumps(payload))

        return HttpResponse(r.text)

    return render_to_response('website/hola.html', {})

@login_required(login_url='/admin')
def usuarios_chat(solicitud):
    from pymongo import Connection

    conn = Connection()

    db = conn[settings.CHAT_DB]
    users = []
    for u in db.users.find():
        if u['name'] is None: continue

        users.append({
            'name': u['name'],
            'red': u['red'],
            'messages': db.messages.find({ 'user.name' : u['name'] }).count(),
        })

    return render_to_response('website/usuarios_chat.html', { 'usuarios': simplejson.dumps(users) })


def conferencia(solicitud, template):
    if template:
        try:
            return render_to_response('%s.html' % template)
        except TemplateDoesNotExist:
            return render_to_response('default.html')        

    try:
        return render_to_response('%s.html' % slugify(get_pais(solicitud.META)))
    except TemplateDoesNotExist:
        return render_to_response('default.html')

@require_POST
def conferencia_registro(solicitud):
    if settings.DEBUG: return HttpResponse()

    asunto = 'Inscripción a la conferencia'

    if solicitud.POST.get('asunto'): asunto = solicitud.POST.get('asunto')

    if not solicitud.POST.get('nombre') or not solicitud.POST.get('email'): return HttpResponse()

    try:
        registro = RegistroConferencia(nombre=solicitud.POST.get('nombre'), email=solicitud.POST.get('email'), pais=get_pais(solicitud.META))
        registro.save()
    except:
        return HttpResponse('FAIL')

    if solicitud.POST.get('extended') == 'viaje':
        send_mail(asunto, u'Nombre: %s\nApellidos: %s\nEmail: %s\nSexo: %s\nTipo de habitación: %s\nTeléfono: %s\nUsuario de Twitter: %s\nComentario: %s\n' % (solicitud.POST.get('nombre'), solicitud.POST.get('apellidos'), solicitud.POST.get('email'), solicitud.POST.get('sexo'), solicitud.POST.get('tipo'), solicitud.POST.get('telefono'), solicitud.POST.get('twitter'), solicitud.POST.get('comentario')), settings.FROM_CONFERENCIA_EMAIL, settings.TO_CONFERENCIA_EMAIL)
    else:    
        send_mail(asunto, 'Nombre: %s\nEmail: %s\n' % (solicitud.POST.get('nombre'), solicitud.POST.get('email')), settings.FROM_CONFERENCIA_EMAIL, settings.TO_CONFERENCIA_EMAIL)

    return HttpResponse('OK')

@require_POST
def conferencia_registro2(solicitud):
    if settings.DEBUG: return HttpResponse()

    asunto = 'Inscripción a la conferencia'

    if solicitud.POST.get('asunto'): asunto = solicitud.POST.get('asunto')

    if not solicitud.POST.get('nombre') or not solicitud.POST.get('email'): return HttpResponse()

    try:
        registro = RegistroConferencia(nombre=solicitud.POST.get('nombre'), email=solicitud.POST.get('email'), pais=get_pais(solicitud.META))
        registro.save()
    except:
        return HttpResponse('FAIL')

    if solicitud.POST.get('extended') == 'viaje':
        send_mail(asunto, u'Nombre: %s\nApellidos: %s\nEmail: %s\nSexo: %s\nTipo de habitación: %s\nTeléfono: %s\nUsuario de Twitter: %s\nComentario: %s\n' % (solicitud.POST.get('nombre'), solicitud.POST.get('apellidos'), solicitud.POST.get('email'), solicitud.POST.get('sexo'), solicitud.POST.get('tipo'), solicitud.POST.get('telefono'), solicitud.POST.get('twitter'), solicitud.POST.get('comentario')), settings.FROM_CONFERENCIA_EMAIL, settings.TO_CONFERENCIA_EMAIL)
    else:    
        send_mail(asunto, 'Nombre: %s\nEmail: %s\n' % (solicitud.POST.get('nombre'), solicitud.POST.get('email')), settings.FROM_CONFERENCIA_EMAIL, settings.TO_CONFERENCIA_EMAIL)

    # por si el usuario esta detras de un proxy
    if solicitud.META.get('HTTP_X_FORWARDED_FOR'):
        ip = solicitud.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = solicitud.META['REMOTE_ADDR']

    pais   = get_pais(solicitud.META)
    
    payload = {
        'email_address': solicitud.POST.get('email'),
        'apikey': settings.MAILCHIMP_APIKEY,
        'merge_vars': {
            'FNAME': solicitud.POST.get('nombre'),
            'OPTINIP': ip,
            'OPTIN_TIME': time.time(),
            'PAIS': pais
        },
        'id': settings.MAILCHIMP_LISTID2,
        'email_type': 'html'
    }

    r = requests.post('http://us2.api.mailchimp.com/1.3/?method=listSubscribe', simplejson.dumps(payload))
    
    return HttpResponse('OK')

def track(solicitud, registro_id):
    registro = get_object_or_404(RegistroCurso, id=registro_id)

    return render_to_response('website/track.html', {'registro': registro })


def podcast(solicitud):
    return render_to_response('website/podcast.html', {
        'podcast_list': Video.objects.all().order_by('-fecha').filter(activado=True).exclude(audio='')
     })