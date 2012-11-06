from django.conf.urls import patterns, url

urlpatterns = patterns('',
	# home de administrador
	url(r'^$', 'edmin.views.admin'),

	### URLS DE ADMINISTRACION DE CURSOS
	url(r'^curso/?$', 'edmin.views.curso'),

	# urls de edicion de cursos
	url(r'^curso/add/?$', 'edmin.views.curso_add'),
	url(r'^curso/edit/(?P<curso_id>\d+)/?$', 'edmin.views.curso_edit'),
	url(r'^curso/delete/(?P<curso_id>\d+)/?$', 'edmin.views.curso_delete'),

	# urls de edicion de docentes
	url(r'^docente/add/(?P<curso_id>\d+)/?$', 'edmin.views.docente_add'),
	url(r'^docente/edit/(?P<docente_id>\d+)/?$', 'edmin.views.docente_edit'),
	url(r'^docente/delete/(?P<docente_id>\d+)/?$', 'edmin.views.docente_delete'),

	# urls de edicion de dia
	url(r'^dia/add/(?P<curso_id>\d+)/?$', 'edmin.views.dia_add'),
	url(r'^dia/edit/(?P<dia_id>\d+)/?$', 'edmin.views.dia_edit'),
	url(r'^dia/delete/(?P<dia_id>\d+)/?$', 'edmin.views.dia_delete'),
)
