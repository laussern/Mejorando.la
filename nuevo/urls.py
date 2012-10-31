from django.conf.urls import patterns, url

urlpatterns = patterns('',
	
	# urls de vista publica de curso
	url(r'^(?P<curso_slug>[\w\d\-]+)/?$', 'nuevo.views.curso'),
)

