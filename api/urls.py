from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^cursos\.json$', 'api.views.cursos'), # archivo de cursos
	url(r'^videos\.json$', 'api.views.videos'), # archivo de videos
)
