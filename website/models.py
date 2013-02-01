# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
import image


# para guardar opciones del sitio (aka switches)
class Setting(models.Model):
    value = models.BooleanField(default=False)
    key = models.CharField(max_length=50)

    def __unicode__(self):
        return self.key


# el archivo de videos
class Video(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.CharField(max_length=300)
    imagen = models.ImageField(blank=True, upload_to='videos')
    fecha = models.DateField()
    embed_code = models.TextField(blank=True)
    descripcion = models.TextField()
    participantes = models.TextField(blank=True)
    activado = models.BooleanField(default=False)
    podcast = models.BooleanField(default=False)
    proximo = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)

        if not self.id or not self.imagen:
            return

        image.resize(image.THUMB, self.imagen)
        image.resize(image.SINGLE, self.imagen)
        image.resize(image.HOME, self.imagen)

    # el permalink
    def get_absolute_url(self):
        return '/videos/%s/' % self.slug

    # los diferentes imagenes para el sitio
    def get_home_image_url(self):
        if not self.imagen:
            return ''

        return image.get_url_by(image.HOME, self.imagen)

    def get_thumb_image_url(self):
        if not self.imagen:
            return ''

        return image.get_url_by(image.THUMB, self.imagen)

    def get_single_image_url(self):
        if not self.imagen:
            return ''

        return image.get_url_by(image.SINGLE, self.imagen)

    def get_invitados(self):
        return VideoInvitado.objects.filter(videos=self)


class VideoInvitado(models.Model):
    nombre  = models.CharField(max_length=500)
    twitter = models.CharField(max_length=300)
    perfil  = models.TextField()
    imagen  = models.ImageField(upload_to='video_invitados')
    videos  = models.ManyToManyField(Video, blank=True)

    def __unicode__(self):
        return self.nombre

    def get_imagen(self):
        return '%s%s' % (settings.MEDIA_URL, self.imagen)

    def save(self, *args, **kwargs):
        super(VideoInvitado, self).save(*args, **kwargs)

        if not self.id and not self.imagen:
            return

        image.resize((100, 100), self.imagen)

# comentarios de los videos
class VideoComentario(models.Model):
    autor_email = models.EmailField()
    autor_url = models.URLField(blank=True)
    autor = models.CharField(max_length=150)
    fecha = models.DateField(auto_now_add=True)
    content = models.TextField()
    video = models.ForeignKey(Video)
    activado = models.BooleanField(default=True)
    ip = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return '%s dijo: %s' % (self.autor, self.content[:100])


class VideoComentarioSpamIP(models.Model):
    ip = models.CharField(max_length=50)

    def __unicode__(self):
        return self.ip


# el formulario para agregar un comentario al video
class VideoComentarioForm(ModelForm):
	class Meta:
		model  = VideoComentario
		fields = ('autor', 'autor_email', 'autor_url', 'content')


# el archivo de cursos
class Curso(models.Model):
    titulo 		  = models.CharField(max_length=150)
    slug	      = models.CharField(max_length=300)
    imagen 	      = models.ImageField(upload_to='cursos')
    pais          = models.CharField(max_length=150)
    fecha 	      = models.DateField()
    descripcion   = models.TextField()
    activado      = models.BooleanField(default=False)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super(Curso, self).save(*args, **kwargs)

        if not self.id and not self.imagen:
            return

        image.resize(image.THUMB, self.imagen)

    def get_thumb_image_url(self):
        return image.get_url_by(image.THUMB, self.imagen)

    def get_image_url(self):
        return '%s%s' % (settings.MEDIA_URL, str(self.imagen))

class Conferencia(models.Model):
    titulo           = models.CharField(max_length=150)
    imagen           = models.ImageField(upload_to='conferencias')
    ubicacion        = models.TextField()
    pais             = models.CharField(max_length=150)
    fecha            = models.DateField()
    descripcion      = models.TextField()
    num_asistentes   = models.IntegerField()
    num_horas_video  = models.IntegerField()
    num_conferencias = models.IntegerField()
    activado         = models.BooleanField(default=False)


    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super(Conferencia, self).save(*args, **kwargs)

        if not self.id and not self.imagen:
            return

        image.resize(image.THUMB, self.imagen)

    def get_thumb_image_url(self):
        return image.get_url_by(image.THUMB, self.imagen)

    def get_image_url(self):
        return '%s%s' % (settings.MEDIA_URL, str(self.imagen))


class RegistroCurso(models.Model):
    nombre    = models.CharField(max_length=500)
    email     = models.EmailField()
    telefono  = models.CharField(max_length=300)
    pago      = models.BooleanField(default=False)
    curso     = models.TextField()
    pais      = models.CharField(max_length=100)
    code      = models.CharField(max_length=100)
    personas  = models.IntegerField(default=1)
    total     = models.FloatField()
    descuento = models.FloatField()
    tipo      = models.CharField(max_length=100, default="paypal")
    fecha     = models.DateField(auto_now_add=True)
    currency  = models.CharField(max_length=10)

    def __unicode__(self):
        return '%s en %s' % (self.nombre, self.curso)


class RegistroConferencia(models.Model):
    nombre    = models.CharField(max_length=500)
    email     = models.EmailField(unique=True)
    pais      = models.CharField(max_length=100)
    fecha     = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.nombre


class MailRegistroCurso(models.Model):
    TIPOS = (
        ('REG', 'Registro'),
        ('INS', 'Instrucción'),
        ('PAG', 'Pago'),
    )

    subject = models.CharField(max_length=500)
    content = models.TextField()
    code    = models.CharField(max_length=100)
    tipo    = models.CharField(max_length=3, choices=TIPOS)

    def __unicode__(self):
        return self.subject


# hooks
def registro_post_save(sender, instance, created, *args, **kwargs):
    if settings.DEBUG:
        return

    if created:
        send_mail('Registro al "%s"' % instance.curso, 'Nombre: %s\nEmail: %s\nTelefono: %s\nTipo de pago: %s\nCurso: %s\nPais: %s\nLink: http://mejorando.la/track/%s\n' % (instance.nombre, instance.email, instance.telefono, instance.tipo, instance.curso, instance.pais, instance.id), settings.FROM_CURSOS_EMAIL, settings.TO_CURSOS_EMAIL)

        try:
            mail = MailRegistroCurso.objects.get(code=instance.code, tipo='REG')

            # mail confirmando registro
            send_mail(mail.subject, u'%s\nTambién puedes realizar tu pago en http://mejorando.la/track/%s\n' % (mail.content, instance.id), settings.FROM_CURSOS_EMAIL, [instance.email])
        except MailRegistroCurso.DoesNotExist:
            pass

        if instance.tipo == 'deposito':
            try:
                mail_inst = MailRegistroCurso.objects.get(code=instance.code, tipo='INS')

                # mail con instrucciones de deposito
                send_mail(mail_inst.subject, mail_inst.content, settings.FROM_CURSOS_EMAIL, [instance.email])
            except MailRegistroCurso.DoesNotExist:
                pass

    if instance.pago:
        send_mail('Pago de "%s"' % instance.curso, '%s (%s) ha realizado el pago de %s por %s persona(s) mediante paypal al "%s"' % (instance.nombre, instance.email, instance.total, instance.personas, instance.curso), settings.FROM_CURSOS_EMAIL, settings.TO_CURSOS_EMAIL)

        try:
            mail_pago = MailRegistroCurso.objects.get(code=instance.code, tipo='PAG')

            # mail confirmando el pago
            send_mail(mail_pago.subject, mail_pago.content, settings.FROM_CURSOS_EMAIL, [instance.email])
        except MailRegistroCurso.DoesNotExist:
            pass

post_save.connect(registro_post_save, sender=RegistroCurso)
