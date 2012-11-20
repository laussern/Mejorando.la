from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models.signals import post_save

import requests

import image
from utils import send_mail, calculate

class Curso(models.Model):
	nombre 	    = models.TextField()
	slug        = models.TextField()
	precio 	    = models.IntegerField()
	pais   	    = models.CharField(max_length=50)
	direccion   = models.TextField()
	mapa 	    = models.CharField(max_length=50, blank=True)
	imagen      = models.ImageField(upload_to='cursos_curso')
	descripcion = models.TextField()
	info_pago   = models.TextField()

	def __unicode__(self):
		return self.nombre 

	# media del curso
	def get_imagen(self):
		return '%s%s' % (settings.MEDIA_URL, self.imagen)

	def get_map_link(self):
		return 'https://maps.google.com/maps?q=%s, %s' % (self.direccion, self.pais)

	def get_map_image(self):
		return 'http://maps.googleapis.com/maps/api/staticmap?size=335x125&maptype=roadmap&markers=icon:http://mejorando.la/nuevaVenta/images/marker.png%7C'+self.mapa+'&zoom=17&sensor=false'

	# variables externas del curso
	def dias(self):      return CursoDia.objects.filter(curso=self)
	def docentes(self):  return CursoDocente.objects.filter(curso=self)
	def registros(self): return CursoRegistro.objects.filter(curso=self)
	def fecha(self):
		dias = CursoDia.objects.filter(curso=self)
		
		if dias.count() > 0: return dias[0].fecha

		return None

	# opciones del curso
	def is_online(self): return self.pais.lower() == 'online'

	def transacciones(self):
		return CursoPago.objects.filter(curso=self)
		
	def pagados(self):
		return CursoPago.objects.filter(charged=True, curso=self)
	def no_pagados(self):
		return CursoPago.objects.filter(charged=False, curso=self)
	def registros(self):
		return CursoRegistro.objects.filter(pago__curso=self)
	def vendidos(self):
		result = CursoPago.objects.filter(charged=True, curso=self).aggregate(models.Sum('quantity'))['quantity__sum']

		if result is None: result = 0
		return result
	def noregistros(self):
		return self.vendidos() - self.registros().count()

	def stripe_total(self):
		return self.stripe_pagados().count() + self.stripe_no_pagados().count()
	def stripe_pagados(self):
		return CursoPago.objects.filter(charged=True, method='card', curso=self)
	def stripe_no_pagados(self):
		return CursoPago.objects.filter(charged=False, method='card', curso=self)
	def stripe_registros(self):
		return CursoRegistro.objects.filter(pago__curso=self, pago__method='card')

	def paypal_total(self):
		return self.paypal_pagados().count() + self.paypal_no_pagados().count()
	def paypal_pagados(self):
		return CursoPago.objects.filter(charged=True, method='paypal', curso=self)
	def paypal_no_pagados(self):
		return CursoPago.objects.filter(charged=False, method='paypal', curso=self)
	def paypal_registros(self):
		return CursoRegistro.objects.filter(pago__curso=self, pago__method='paypal')

	def deposit_total(self):
		return self.deposit_pagados().count() + self.deposit_no_pagados().count()
	def deposit_pagados(self):
		return CursoPago.objects.filter(charged=True, method='deposit', curso=self)
	def deposit_no_pagados(self):
		return CursoPago.objects.filter(charged=False, method='deposit', curso=self)
	def deposit_registros(self):
		return CursoRegistro.objects.filter(pago__curso=self, pago__method='deposit')

	
	def regions(self):
		r = []

		for p in CursoRegistro.objects.filter(pago__curso=self, pago__charged=True).values('pago__pais').annotate(models.Count('id')):
			r.append([p['pago__pais'], p['id__count']])
		
		return simplejson.dumps(r)

	def timeline(self):
		pagos = CursoPago.objects.filter(charged=True, curso=self)

		return simplejson.dumps([ [ f.strftime('%b/%d'), pagos.filter(fecha__year=f.year, fecha__month=f.month, fecha__day=f.day).count() ] for f in pagos.dates('fecha', 'day')])

	def save(self, *args, **kwargs):
		super(Curso, self).save(*args, **kwargs)

		return

		if not self.id and not self.imagen: return

		image.resize((666, 430), self.imagen)

class CursoDia(models.Model):
	fecha 	= models.DateTimeField()
	tema  	= models.CharField(max_length=500)
	temario = models.TextField()
	curso   = models.ForeignKey(Curso)

	def __unicode__(self):
		return self.tema

class CursoDocente(models.Model):
	nombre  = models.CharField(max_length=500)
	twitter = models.CharField(max_length=300)
	perfil  = models.TextField()
	imagen  = models.ImageField(upload_to='cursos_docentes')
	curso   = models.ForeignKey(Curso, blank=True)

	def __unicode__(self):
		return self.nombre

	def get_imagen(self):
		return '%s%s' % (settings.MEDIA_URL, self.imagen)

	def save(self, *args, **kwargs):
		super(CursoDocente, self).save(*args, **kwargs)

		if not self.id and not self.imagen: return

		image.resize((67, 67), self.imagen)

class CursoPago(models.Model):
	TIPOS = (
		('card', 'Stripe'),
		('paypal', 'PayPal'),
		('deposit', 'Deposito')
	)

	nombre 	 = models.CharField(max_length=500)
	email  	 = models.EmailField()
	telefono = models.CharField(max_length=500)
	pais     = models.CharField(max_length=100)
	quantity = models.IntegerField()
	fecha    = models.DateTimeField(auto_now_add=True)
	curso    = models.ForeignKey(Curso)
	charged  = models.BooleanField(default=False)
	method   = models.CharField(max_length=10, choices=TIPOS)
	error 	 = models.CharField(max_length=200, blank=True)

	def intentos(self):
		return CursoPago.objects.filter(email=self.email, curso=self.curso, method=self.method).count()

	def __unicode__(self):
		return '%s - %s ' % (self.nombre, self.email)

class CursoRegistro(models.Model):
	email  	 = models.EmailField()
	pago     = models.ForeignKey(CursoPago)

	def __unicode__(self):
		return self.email

# HOOKS
def create_pago(sender, instance, created, *args, **kwargs):
	curso = instance.curso

	if created and instance.method == 'deposit':
		send_mail('curso_info', { 'curso': curso }, 'Informacion para realizar pago al %s de Mejorando.la INC' % curso.nombre, instance.email)

	if instance.charged:
		vs = calculate(int(instance.quantity), curso.precio)

		vs['curso'] = curso
		vs['pago']  = instance

		send_mail('curso_pago', vs, 'Gracias por tu pago al %s de Mejorando.la INC' % curso.nombre, instance.email)

def create_registro(sender, instance, created, *args, **kwargs):
	if created:
		# integracion con la plataforma
		curso = instance.pago.curso

		try:
			r = requests.post(u'%spreregistro' % settings.PLATAFORMA_API_URL, { 'slug': curso.slug, 'email': instance.email, 'passwd': settings.PLATAFORMA_API_KEY })
		except: pass

post_save.connect(create_pago, sender=CursoPago)
post_save.connect(create_registro, sender=CursoRegistro)