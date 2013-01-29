from django.conf.urls.defaults import patterns, url
from feeds import VideoFeed

urlpatterns = patterns('',
    # home
    url(r'^$',         'website.views.home'),
    # archivo de videos
    url(r'^videos/?$', 'website.views.videos'),
    # video individual
    url(r'^videos/(?P<video_slug>.+?)/?$', 'website.views.video'),
    # transmision en vivo
    url(r'^live/?$',   'website.views.live'),
    # feed de videos
    url(r'^feed/?$', VideoFeed(), name='feed'),
    # servicio de localizacion
    url(r'^locateme/?$', 'website.views.locateme'),
    # suscripcion a las listas de correo
    url(r'^hola/?$', 'website.views.hola'),
    url(r'^conferencia/(?P<template>.*?)/?$', 'website.views.conferencia'),
    # podcast de mejorandola
    url(r'^podcast/?$', 'website.views.podcast'),

    url(r'^(?P<path>conferencias)/?$', 'website.views.all'),
    url(r'^(?P<path>espana)/?$', 'website.views.all'),
    url(r'^(?P<path>guia-html5)/?$', 'website.views.all'),
    url(r'^(?P<path>privacidad)/?$', 'website.views.all'),
    url(r'^(?P<path>respuesta)/?$', 'website.views.all'),
    url(r'^(?P<path>terminos)/?$', 'website.views.all'),
    url(r'^(?P<path>sponsors/bilingham)/?$', 'website.views.all'),
)
