from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'cursos.views.home'),

    # urls de notificacion de pago de paypal
    url(r'^paypal_ipn/?$', 'cursos.views.paypal_ipn'),

    # urls de vista publica de cursos
    url(r'^(?P<curso_slug>[\w\d\-]+)/?$', 'cursos.views.curso'),
)
