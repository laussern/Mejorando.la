from django.db import models
from django.conf import settings
import image

class Curso(models.Model):
	nombre 	    = models.TextField()
	slug        = models.TextField()
	precio 	    = models.CharField(max_length=30)
	pais   	    = models.CharField(max_length=50)
	direccion   = models.TextField()
	mapa 	    = models.CharField(max_length=50, blank=True)
	imagen      = models.ImageField(upload_to='nuevo_curso')
	moneda      = models.CharField(max_length=10)
	descripcion = models.TextField()

	def __unicode__(self):
		return self.nombre 

	def get_imagen(self):
		return '%s%s' % (settings.MEDIA_URL, self.imagen)

	def get_pais_imagen(self):
		return ''

	def dias(self):
		return CursoDia.objects.filter(curso=self)

	def docentes(self):
		return CursoDocente.objects.filter(curso=self)

	def save(self, *args, **kwargs):
		super(Curso, self).save(*args, **kwargs)

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
	imagen  = models.ImageField(upload_to='nuevo_docentes')
	curso   = models.ForeignKey(Curso)

	def __unicode__(self):
		return self.nombre

	def get_imagen(self):
		return '%s%s' % (settings.MEDIA_URL, self.imagen)

	def save(self, *args, **kwargs):
		super(CursoDocente, self).save(*args, **kwargs)

		if not self.id and not self.imagen: return

		image.resize((67, 67), self.imagen)

class CursoRegistro(models.Model):
	nombre 	 = models.CharField(max_length=500)
	email  	 = models.EmailField()
	telefono = models.CharField(max_length=500)
	pais     = models.CharField(max_length=100)
	pagado   = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nombre

	