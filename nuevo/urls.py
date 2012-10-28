from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^admin/?$', 'nuevo.views.admin'),
	url(r'^admin/add/?$', 'nuevo.views.admin_add'),
	url(r'^admin/edit/(?P<curso_slug>[\w\d\-]+)/?$', 'nuevo.views.admin_edit'),
	url(r'^(?P<curso_slug>[\w\d\-]+)/?$', 'nuevo.views.curso'),
)

