from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def send_mail(tipo, vs, subject, email):
	html_content = render_to_string('cursos/email/%s.html' % tipo, vs)
	mail = EmailMultiAlternatives(subject,
		strip_tags(html_content), 'Cursos Mejorando.la <ventas@mejorando.la>', [email])

	mail.attach_alternative(html_content, 'text/html')
	mail.send()