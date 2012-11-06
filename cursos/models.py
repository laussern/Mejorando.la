from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
import image

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
	nombre 	 = models.CharField(max_length=500)
	email  	 = models.EmailField()
	telefono = models.CharField(max_length=500)
	pais     = models.CharField(max_length=100)
	quantity = models.IntegerField()
	fecha    = models.DateTimeField(auto_now_add=True)
	curso    = models.ForeignKey(Curso)
	charged  = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nombre

class CursoRegistro(models.Model):
	email  	 = models.EmailField()
	pago     = models.ForeignKey(CursoPago)

	def __unicode__(self):
		return self.email

	