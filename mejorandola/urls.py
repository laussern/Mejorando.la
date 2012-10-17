from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from feeds import VideoFeed

admin.autodiscover()

handler404 = 'website.views.handler404'

urlpatterns = patterns('',
	url(r'^$', 		   'website.views.home'), # home
    url(r'^cursos/?$', 'website.views.cursos'), # archivo de cursos
	url(r'^videos/?$', 'website.views.videos'), # archivo de videos
	url(r'^videos/(?P<video_slug>.+?)/?$', 'website.views.video'), # video individual
    url(r'^live/?$',   'website.views.live'),  # transmision en vivo

    url(r'^feed/?$', VideoFeed(), name='feed'), # feed de videos

    url(r'^regenerate/?$', 'website.views.regenerate'),

    # actualizar el codigo
    url(r'^update/?$', 'github.views.update'),

    # registro y pago de cursos
    url(r'^cursos/registro$', 'website.views.cursos_registro'),
    url(r'^cursos/pago/success$', 'website.views.cursos_pago_success'),
    url(r'^cursos/registros$', 'website.views.cursos_registros'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^locateme/?$', 'website.views.locateme'),

    url(r'^hola/?$', 'website.views.hola'),

    url(r'^usuarios_chat$', 'website.views.usuarios_chat'),

    url(r'^conferencia/(?P<template>.*?)/?$', 'website.views.conferencia'),

    url(r'^conferencia_registro/?$', 'website.views.conferencia_registro'),
    url(r'^conferencia_registro2/?$', 'website.views.conferencia_registro2'),

    url(r'^track/(?P<registro_id>\d+?)$', 'website.views.track'),

    url(r'^nuevo/', include('nuevo.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
