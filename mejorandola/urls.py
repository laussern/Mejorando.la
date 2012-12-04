from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from feeds import VideoFeed

admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', 		   'website.views.home'), # home
	url(r'^videos/?$', 'website.views.videos'), # archivo de videos
    url(r'^conferencias/?$', 'website.views.conferencias'), # archivo de conferencias
	url(r'^videos/(?P<video_slug>.+?)/?$', 'website.views.video'), # video individual
    #url(r'^live/?$',   'website.views.live'),  # transmision en vivo

    url(r'^feed/?$', VideoFeed(), name='feed'), # feed de videos

    url(r'^regenerate/?$', 'website.views.regenerate'),

    # actualizar el codigo
    url(r'^update/?$', 'github.views.update'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^locateme/?$', 'website.views.locateme'),

    url(r'^hola/?$', 'website.views.hola'),

    url(r'^usuarios_chat$', 'website.views.usuarios_chat'),

    url(r'^conferencia/(?P<template>.*?)/?$', 'website.views.conferencia'),

    url(r'^conferencia_registro/?$', 'website.views.conferencia_registro'),
    url(r'^conferencia_registro2/?$', 'website.views.conferencia_registro2'),

    url(r'^track/(?P<registro_id>\d+?)$', 'website.views.track'),

    url(r'^cursos/', include('cursos.urls')),
    url(r'^edmin/', include('edmin.urls')),
    url(r'^api/', include('api.urls')),

    url(r'^podcast/?$', 'website.views.podcast'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
