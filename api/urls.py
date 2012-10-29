from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^cursos/?$', 'api.views.cursos'), # archivo de cursos
	url(r'^videos/?$', 'api.views.videos'), # archivo de videos
	url(r'^videos/(?P<video_slug>.+?)/?$', 'api.views.video'), # video individual
)
