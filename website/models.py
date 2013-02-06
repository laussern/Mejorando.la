# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

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

    def get_podcast_url(self):
        return '/podcasts/%s.mp3' % self.slug

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


class VideoInvitado(models.Model):
    nombre = models.CharField(max_length=500)
    twitter = models.CharField(max_length=300)
    perfil = models.TextField()
    imagen = models.ImageField(upload_to='video_invitados')
    videos = models.ManyToManyField(Video, blank=True)

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
    autor_image_url = models.URLField(blank=True)
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


# el archivo de cursos
class Curso(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.CharField(max_length=300)
    imagen = models.ImageField(upload_to='cursos')
    pais = models.CharField(max_length=150)
    fecha = models.DateField()
    descripcion = models.TextField()
    activado = models.BooleanField(default=False)

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

    def get_absolute_url(self):
        return '/cursos/' % self.slug

    def get_flag_image_url(self):
        return '/static/images/home/%s.jpg' % slugify(self.pais)
