from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^(?P<curso_slug>[\w\d\-]+)/?$', 'nuevo.views.curso'),
)

