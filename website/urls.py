from django.conf.urls.defaults import patterns, url
from feeds import VideoFeed

urlpatterns = patterns('',
    # home
    url(r'^$',         'website.views.home'),
    # archivo de videos
    url(r'^videos/?$', 'website.views.videos'),
    # archivo de conferencias
    url(r'^conferencias/?$', 'website.views.conferencias'),
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

    url(r'^(?P<path>.*?)/?$', 'website.views.all'),
)
